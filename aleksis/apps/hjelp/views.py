from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from rules.contrib.views import permission_required
from templated_email import send_templated_mail

from aleksis.core.models import Activity
from aleksis.core.util.core_helpers import get_site_preferences

from .forms import FAQForm, FeedbackForm, IssueForm
from .models import FAQQuestion, FAQSection, IssueCategory


@permission_required("hjelp.view_faq")
def faq(request):
    """ Shows the FAQ page """

    context = {
        "questions": FAQQuestion.objects.filter(show=True),
        "sections": FAQSection.objects.all(),
    }
    return render(request, "hjelp/faq.html", context)


@permission_required("hjelp.ask_faq")
def ask_faq(request):
    if request.method == "POST":
        form = FAQForm(request.POST)
        if form.is_valid():
            # Read out form data
            question = form.cleaned_data["question"]

            act = Activity(
                title=_("You have submitted a question."),
                description=question,
                app="Hjelp",
                user=request.user,
            )
            act.save()

            context = {
                "description": [question],
                "user": request.user,
                "type": _("FAQ question"),
            }
            send_templated_mail(
                template_name="hjelp",
                from_email=f"{request.user.get_full_name()} <{request.user.email}>",
                recipient_list=[get_site_preferences()["hjelp__faq_recipient"]],
                context=context,
            )

            return render(request, "hjelp/question_submitted.html")
    else:
        form = FAQForm()

    return render(request, "hjelp/ask.html", {"form": form})


def add_arrows(array: list):
    return " → ".join([item for item in array if item != ""])


def issues_get_next_properties(request):
    category = request.GET.get("category", None)
    next_properties = {
        "icon": IssueCategory.objects.get(name=category).icon,
        "free_text": IssueCategory.objects.get(name=category).free_text,
        "placeholder": IssueCategory.objects.get(name=category).placeholder,
        "has_children": IssueCategory.objects.get(name=category).children.exists(),
    }
    return JsonResponse(next_properties)


@permission_required("hjelp.report_issue")
def report_issue(request):
    if request.method == "POST":
        form = IssueForm(request.POST)
        if form.is_valid():
            # Read out form data
            bug_category_1 = str(form.cleaned_data["bug_category_1"])
            bug_category_2 = str(form.cleaned_data["bug_category_2"])
            bug_category_3 = str(form.cleaned_data["bug_category_3"])
            bug_category_free_text = form.cleaned_data["bug_category_free_text"]
            short_description = form.cleaned_data["short_description"]
            long_description = form.cleaned_data["long_description"]

            # Register activity
            desc_categories = add_arrows(
                [bug_category_1, bug_category_2, bug_category_3, bug_category_free_text,]
            )
            desc_act = f"{desc_categories} | {short_description}"
            act = Activity(
                title=_("You reported a problem."),
                description=desc_act,
                app="Hjelp",
                user=request.user,
            )
            act.save()

            # Send mail
            context = {
                "description": [
                    add_arrows(
                        [bug_category_1, bug_category_2, bug_category_3, bug_category_free_text,]
                    ),
                    short_description,
                    long_description,
                ],
                "user": request.user,
                "type": _("Issue"),
            }
            send_templated_mail(
                template_name="hjelp",
                from_email=f"{request.user.get_full_name()} <{request.user.email}>",
                recipient_list=[get_site_preferences()["hjelp__issue_report_recipient"]],
                context=context,
            )

            return render(request, "hjelp/issue_report_submitted.html")
    else:
        form = IssueForm()

    return render(request, "hjelp/issue_report.html", {"form": form})


@permission_required("hjelp.send_feedback")
def feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Read out form data
            design_rating = form.cleaned_data["design_rating"]
            performance_rating = form.cleaned_data["performance_rating"]
            usability_rating = form.cleaned_data["usability_rating"]
            overall_rating = form.cleaned_data["overall_rating"]
            more = form.cleaned_data["more"]
            ideas = form.cleaned_data["ideas"]
            apps = form.cleaned_data["apps"]

            # Register activity
            act = Activity.objects.create(
                title=_("You submitted feedback."),
                description=_(f"You rated AlekSIS with {overall_rating} from 5 stars."),
                app="Feedback",
                user=request.user,
            )

            # Send mail
            context = {
                "description": [
                    design_rating,
                    performance_rating,
                    usability_rating,
                    overall_rating,
                    more,
                    apps,
                    ideas,
                ],
                "user": request.user,
                "type": _("Feedback"),
            }
            send_templated_mail(
                template_name="hjelp",
                from_email=f"{request.user.get_full_name()} <{request.user.email}>",
                recipient_list=[get_site_preferences()["hjelp__feedback_recipient"]],
                context=context,
            )

            return render(request, "hjelp/feedback_submitted.html")
    else:
        form = FeedbackForm()

    return render(request, "hjelp/feedback.html", {"form": form})
