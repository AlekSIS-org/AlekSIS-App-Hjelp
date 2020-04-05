from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from .models import FAQSection, FAQQuestion
from .forms import FAQForm, REBUSForm, FeedbackForm

from datetime import datetime
from constance import config


from .mailer import send_mail_with_template

from aleksis.apps.chronos.models import Room
from aleksis.core.models import Activity


def create_info(text):
    return '<div class="alert success"> <p> <i class="material-icons left">info</i>' + text + '</p> </div>'


def faq(request):
    """ Shows the FAQ site, also if not logged in"""
    context = {
        "questions": FAQQuestion.objects.filter(show=True),
        "sections": FAQSection.objects.all(),
    }
    return render(request, 'hjelp/faq.html', context)


@login_required
def ask(request):
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            # Read out form data
            question = form.cleaned_data['question']

            act = Activity(title=_("You have submitted a question."), description=question, app="Hjelp",
                          user=request.user)
            act.save()

            context = {
                "question": question,
                "user": request.user
            }
            send_mail_with_template("[FAQ QUESTION] {}".format(question), [config.MAIL_QUESTIONS],
                                    "hjelp/mail/question.txt",
                                    "hjelp/mail/question.html", context,
                                    "{} <{}>".format(request.user.get_full_name(), request.user.email))

            return render(request, 'hjelp/question_submitted.html')
    else:
        form = FAQForm()

    return render(request, "hjelp/ask.html", {"form": form})


def add_arrows(array: list):
    return " → ".join([item for item in array if item != ""])


@login_required
def rebus(request):
    if request.method == 'POST':
        form = REBUSForm(request.POST)
        if form.is_valid():
            # Read out form data
            bug_category_1 = str(form.cleaned_data['bug_category_1'])
            bug_category_2 = str(form.cleaned_data['bug_category_2'])
            bug_category_3 = str(form.cleaned_data['bug_category_2'])
            short_description = form.cleaned_data['short_description']
            long_description = form.cleaned_data['long_description']

            # Register activity
            desc_act = "{} | {}".format(add_arrows([bug_category_1, bug_category_2, bug_category_3]), short_description)
            act = Activity(title=_("You reported a problem."), description=desc_act, app="Hjelp",
                           user=request.user)
            act.save()

            # Send mail
            context = {
                "arrow_list": add_arrows([bug_category_1, bug_category_2, bug_category_3]),
                "short_desc": short_description,
                "long_desc": long_description,
                "user": request.user
            }
            send_mail_with_template("[REBUS] {}".format(short_description), [config.MAIL_REBUS],
                                    "hjelp/mail/rebus.txt",
                                    "hjelp/mail/rebus.html", context,
                                    "{} <{}>".format(request.user.get_full_name(), request.user.email))

            return render(request, 'hjelp/rebus_submitted.html')
    else:
        form = REBUSForm()

    rooms = [room.name for room in Room.objects.all()]

    return render(request, 'hjelp/rebus.html', {'form': form, "props": {"rooms": "rooms"}})


@login_required
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Read out form data
            design_rating = form.cleaned_data['design_rating']
            performance_rating = form.cleaned_data['performance_rating']
            usability_rating = form.cleaned_data['usability_rating']
            overall_rating = form.cleaned_data['overall_rating']
            more = form.cleaned_data['more']
            ideas = form.cleaned_data['ideas']
            apps = form.cleaned_data["apps"]

            # Register activity
            act = Activity(title=_("You submitted feedback."),
                           description=_("You rated AlekSIS with {} from 5 stars.").format(
                               overall_rating), app="Feedback",
                           user=request.user)
            act.save()

            # Send mail
            context = {
                "design": design_rating,
                "performance": performance_rating,
                "usability": usability_rating,
                "overall": overall_rating,
                "more": more,
                "apps": apps,
                "ideas": ideas,
                "user": request.user
            }
            send_mail_with_template(_("Feedback from {}").format(request.user.username),
                                    [config.MAIL_FEEDBACK],
                                    "hjelp/mail/feedback.txt",
                                    "hjelp/mail/feedback.html", context,
                                    "{} <{}>".format(request.user.get_full_name(), request.user.email))

            return render(request, 'hjelp/feedback_submitted.html')
    else:
        form = FeedbackForm()

    return render(request, 'hjelp/feedback.html', {'form': form})
