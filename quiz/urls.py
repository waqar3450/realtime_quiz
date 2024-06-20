from django.urls import path
from . import views

urlpatterns = [
    path('<str:quiz_id>/', views.quiz_view, name='quiz_view'),
]