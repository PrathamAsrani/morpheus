from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Form, Response as FormResponse, Answer
from .serializers import FormSerializer, ResponseSerializer, AnswerSerializer, UserSerializer
from django.contrib.auth.models import User

# Create Form API
class CreateFormView(APIView):
    def post(self, request):
        serializer = FormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# List Forms API
class ListFormsView(APIView):
    def get(self, request):
        # Get the user_id from the request (assuming it's sent in the query parameters)
        user_id = request.query_params.get('user_id')
        
        if not user_id:
            return Response({'error': 'User ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if the user exists in the database
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is an admin (superuser)
        if not user.is_superuser:
            return Response({'error': 'You must be an admin to view forms.'}, status=status.HTTP_403_FORBIDDEN)

        # If the user is an admin, retrieve the forms
        forms = Form.objects.all()

        # Serialize the forms
        serializer = FormSerializer(forms, many=True)
        return Response(serializer.data)



class SubmitResponseView(APIView):
    def post(self, request, form_id):
        print(f"Form ID received: {form_id}")  # Add this line for debugging
        try:
            form = Form.objects.get(pk=form_id)
        except Form.DoesNotExist:
            return Response({'error': 'Form not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ResponseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(form=form)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FormAnalyticsView(APIView):
    def get(self, request, form_id):
        try:
            form = Form.objects.get(pk=form_id)
        except Form.DoesNotExist:
            return Response({'error': 'Form not found'}, status=status.HTTP_404_NOT_FOUND)

        responses = form.responses.count()
        questions = form.questions.all()
        analytics = {
            'form_id': form.id,
            'form_title': form.title,
            'total_responses': responses,
            'questions': []
        }

        for question in questions:
            answers = question.answers.all()
            analytics['questions'].append({
                'question_text': question.text,
                'response_count': answers.count(),
                'answers': [{'id': ans.id, 'text': ans.answer_text, 'options': ans.selected_options} for ans in answers]
            })

        return Response(analytics)


class CreateUserView(APIView):
    def post(self, request, *args, **kwargs):
        # Serialize the incoming data
        serializer = UserSerializer(data=request.data)
        
        # Validate and create the user if valid
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'End User created successfully.',
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        # If validation fails, return the error details
        return Response({
            'error': 'Invalid data.',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)