from django.urls import path
from .views import CreateFormView, ListFormsView, SubmitResponseView, FormAnalyticsView, CreateUserView

urlpatterns = [
    path('forms/', CreateFormView.as_view(), name='create_form'),
    path('forms/list/', ListFormsView.as_view(), name='list_forms'),
    path('forms/<int:form_id>/responses/', SubmitResponseView.as_view(), name='submit_response'),
    path('forms/<int:form_id>/analytics/', FormAnalyticsView.as_view(), name='form_analytics'),
    path('auth/create/', CreateUserView.as_view(), name='create_user')
]
