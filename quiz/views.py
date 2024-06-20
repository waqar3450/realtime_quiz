from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def quiz_view(request, quiz_id):
    return render(request, 'quiz_app/quiz.html', {'quiz_id': quiz_id})


