from django.db import models
from django.db.models import JSONField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Form model
class Form(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="forms")

    def clean(self):
        # Ensure that a form can have no more than 100 questions
        if self.questions.count() > 100:
            raise ValidationError('A form cannot have more than 100 questions.')


# Question model
class Question(models.Model):
    TEXT = 'text'
    DROPDOWN = 'dropdown'
    CHECKBOX = 'checkbox'
    QUESTION_TYPES = [
        (TEXT, 'Text'),
        (DROPDOWN, 'Dropdown'),
        (CHECKBOX, 'Checkbox'),
    ]

    form = models.ForeignKey(Form, related_name="questions", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    options = JSONField(blank=True, null=True, help_text="Options for dropdown/checkbox questions.")
    order = models.PositiveIntegerField()

# Response model
class Response(models.Model):
    form = models.ForeignKey(Form, related_name="responses", on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

# Answer model
class Answer(models.Model):
    response = models.ForeignKey(Response, related_name="answers", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True, null=True)  # For text responses
    selected_options = models.TextField(blank=True, null=True, help_text="Comma-separated options for dropdown/checkbox.")
