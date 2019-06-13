from django.shortcuts import render
from faq.models import FAQQuestion, Question
from faq.forms import FAQForm

from datetime import datetime

from dashboard.models import Activity

# Create your views here.

def create_info(text):
    return '<div class="alert success"> <p> <i class="material-icons left">info</i>' + text + '</p> </div>'


def faq(request):
    """ Shows the FAQ site, also if not logged in"""
    context = {
        "questions": FAQQuestion.objects.filter(show=True),
    }
    return render(request, 'faq/faq.html', context)

def ask(request):
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            # Read out form data
            question = form.cleaned_data['question']
            userid = request.user

            new_question = Question(question_text=question, pub_date=datetime.now(), user=userid)

            new_question.save()

            act = Activity(title="Du hast uns eine Frage gestellt.", description=question, app="FAQ",
                           user=userid)
            act.save()

            return render(request, 'faq/question_submitted.html')
    else:
        form = FAQForm()

    return render(request, "faq/ask.html", {"form": form})