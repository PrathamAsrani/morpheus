from rest_framework import serializers
from .models import Form, Question, Response, Answer
from django.contrib.auth.models import User

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'options', 'order']

class FormSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Keep this as is.

    class Meta:
        model = Form
        fields = ['id', 'title', 'created_at', 'questions', 'user']

    def create(self, validated_data):
        user = validated_data.get('user')

        # Check if the user is an admin (superuser)
        if not user.is_superuser:
            raise serializers.ValidationError("You must be a superuser to create a form.")

        questions_data = validated_data.pop('questions')

        form = Form.objects.create(**validated_data)

        for question_data in questions_data:
            Question.objects.create(form=form, **question_data)

        return form


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'answer_text', 'selected_options']

class ResponseSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Response
        fields = ['id', 'form', 'submitted_at', 'answers']

    def create(self, validated_data):
        # Pop the 'answers' data from the validated data
        answers_data = validated_data.pop('answers')
        
        # Create the Response instance
        response = Response.objects.create(**validated_data)
        
        # Create the Answer instances and link them to the response
        for answer_data in answers_data:
            Answer.objects.create(response=response, **answer_data)
        
        return response

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Make password write-only
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user
