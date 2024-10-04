from django.shortcuts import render
from .forms import QuizForm

def quiz_home_view(request):
    return render(request, 'cvsuquiz/quiz_home.html')

def quiz_home(request):
    feedback_q1 = None
    feedback_q2 = None
    feedback_q3 = None


    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            answer_q1 = form.cleaned_data['answer_q1']
            answer_q2 = form.cleaned_data['answer_q2']
            answer_q3 = form.cleaned_data['answer_q3']

            if answer_q1 == '4':
                feedback_q1 = "Correct!"
            else:
                feedback_q1 = "Wrong! The correct answer is D"

            if answer_q2 == 'C':
                feedback_q2 = "Correct!"
            else:
                feedback_q2 = "Wrong! The correct answer is C"

            if answer_q3 == 'C':
                feedback_q3 = "Correct!"
            else:
                feedback_q3 = "Wrong! The correct answer is D"    
    else:
        form = QuizForm()

    return render(request, 'cvsuquiz/cspear.html', {
        'form': form, 
        'feedback_q1': feedback_q1,
        'feedback_q2': feedback_q2,
        'feedback_q3': feedback_q3,
    })