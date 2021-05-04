from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.generic import ListView, UpdateView, FormView
from material import Layout, Row

from rules.contrib.views import permission_required, PermissionRequiredMixin
from templated_email import send_templated_mail

from aleksis.core.models import Activity
from aleksis.core.util.core_helpers import get_site_preferences

from .forms import FAQForm, FAQOrderFormSet, FeedbackForm, IssueForm
from .models import FAQQuestion, FAQSection, IssueCategory


@permission_required("hjelp.view_faq")
def faq(request):
    """Show the FAQ page."""
    context = {
        "sections": FAQSection.objects.filter(show=True),
    }
    return render(request, "hjelp/faq.html", context)


class FAQOrder(PermissionRequiredMixin, FormView):
    queryset = FAQSection.objects.all()
    template_name = "hjelp/order_faq.html"
    form_class = FAQOrderFormSet
    success_url = "#"
    permission_required = "hjelp.change_faq"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["layout"] = Layout(Row("name", "icon", "show"))  # , "ORDER"))

        return context

    def form_valid(self, form):
        for individual_form in form.forms:
            pos = individual_form.cleaned_data["ORDER"]
            individual_form.cleaned_data["position"] = pos
            individual_form.instance.position = pos
            individual_form.instance.save()

        questions_and_sections = zip(self.request.POST.getlist("question-ids[]"),
                                     self.request.POST.getlist("question-sections[]"))

        for question, section in questions_and_sections:
            q = FAQQuestion.objects.get(pk=question)
            q.section = FAQSection.objects.get(pk=section)
            q.save()

        return super().form_valid(form)


@never_cache
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
                user=request.user.person,
            )
            act.save()

            context = {
                "question": question,
                "user": request.user,
            }

            send_templated_mail(
                template_name="faq",
                from_email=request.user.person.mail_sender_via,
                headers={
                    "Reply-To": request.user.person.mail_sender,
                    "Sender": request.user.person.mail_sender,
                },
                recipient_list=[get_site_preferences()["hjelp__faq_recipient"]],
                context=context,
            )

            return render(request, "hjelp/question_submitted.html")
    else:
        form = FAQForm()

    return render(request, "hjelp/ask.html", {"form": form})


def add_arrows(array: list):
    return " → ".join([item for item in array if item != "" and item.lower() != "none"])


@never_cache
def issues_get_next_properties(request):
    category = request.GET.get("category", None)
    next_properties = {
        "icon": IssueCategory.objects.get(name=category).icon,
        "free_text": IssueCategory.objects.get(name=category).free_text,
        "placeholder": IssueCategory.objects.get(name=category).placeholder,
        "has_children": IssueCategory.objects.get(name=category).children.exists(),
    }
    return JsonResponse(next_properties)


@never_cache
@permission_required("hjelp.report_issue")
def report_issue(request):
    if request.method == "POST":
        form = IssueForm(request.POST)
        if form.is_valid():
            # Read out form data
            category_1 = str(form.cleaned_data["category_1"])
            category_2 = str(form.cleaned_data["category_2"])
            category_3 = str(form.cleaned_data["category_3"])
            free_text = form.cleaned_data["free_text"]
            short_description = form.cleaned_data["short_description"]
            long_description = form.cleaned_data["long_description"]

            # Register activity
            desc_categories = add_arrows([category_1, category_2, category_3, free_text,])
            desc_act = f"{desc_categories} | {short_description}"
            act = Activity(
                title=_("You reported a problem."),
                description=desc_act,
                app="Hjelp",
                user=request.user.person,
            )
            act.save()

            # Send mail
            context = {
                "categories": add_arrows([category_1, category_2, category_3, free_text,]),
                "categories_single": (
                    element
                    for element in [category_1, category_2, category_3, free_text,]
                    if element and element != "None"
                ),
                "short_description": short_description,
                "long_description": long_description,
                "user": request.user,
            }
            send_templated_mail(
                template_name="rebus",
                from_email=request.user.person.mail_sender_via,
                headers={
                    "Reply-To": request.user.person.mail_sender,
                    "Sender": request.user.person.mail_sender,
                },
                recipient_list=[get_site_preferences()["hjelp__issue_report_recipient"]],
                context=context,
            )

            return render(request, "hjelp/issue_report_submitted.html")
    else:
        form = IssueForm()

    return render(request, "hjelp/issue_report.html", {"form": form})


@never_cache
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
                description=_(f"You rated AlekSIS with {overall_rating} out of 5 stars."),
                app="Feedback",
                user=request.user.person,
            )

            # Send mail
            context = {
                "design_rating": design_rating,
                "performance_rating": performance_rating,
                "usability_rating": usability_rating,
                "overall_rating": overall_rating,
                "more": more,
                "apps": apps,
                "ideas": ideas,
                "user": request.user,
            }
            send_templated_mail(
                template_name="feedback",
                from_email=request.user.person.mail_sender_via,
                headers={
                    "Reply-To": request.user.person.mail_sender,
                    "Sender": request.user.person.mail_sender,
                },
                recipient_list=[get_site_preferences()["hjelp__feedback_recipient"]],
                context=context,
            )

            return render(request, "hjelp/feedback_submitted.html")
    else:
        form = FeedbackForm()

    return render(request, "hjelp/feedback.html", {"form": form})
