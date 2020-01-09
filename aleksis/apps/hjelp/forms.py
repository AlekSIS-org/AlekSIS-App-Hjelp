from django import forms
from django.utils.translation import ugettext_lazy as _
from django_select2.forms import Select2Widget
from .models import REBUSSelectModel


class FAQForm(forms.Form):
    question = forms.CharField(widget=forms.Textarea(),
                               label=_("Your questions"), required=True)


class REBUSForm_old(forms.Form):
    a = forms.CharField(label=_("Category A"), required=True)
    b = forms.CharField(label=_("Category B"), required=False)
    c = forms.CharField(label=_("Category C"), required=False)
    short_description = forms.CharField(label=_("Please describe the error in one sentence."), required=True)
    long_description = forms.CharField(widget=forms.Textarea, label=_("Please describe the error more detailed."),
                                       required=False)


class FeedbackForm(forms.Form):
    ratings = [(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)]

    design_rating = forms.ChoiceField(label=_("Design of the user interface"),
                                      choices=ratings,
                                      widget=forms.RadioSelect(attrs={"checked": "checked"}),
                                      required=True,
                                      )

    performance_rating = forms.ChoiceField(label=_("Speed"),
                                           choices=ratings,
                                           widget=forms.RadioSelect(attrs={"checked": "checked", "class": "required"}),
                                           required=True)

    usability_rating = forms.ChoiceField(label=_("User friendlines"),
                                         choices=ratings,
                                         widget=forms.RadioSelect(attrs={"checked": "checked"}),
                                         required=True)

    overall_rating = forms.ChoiceField(label=_("AlekSIS in general"),
                                       choices=ratings,
                                       widget=forms.RadioSelect(attrs={"checked": "checked"}),
                                       required=True)

    apps = forms.CharField(
        label=_("What do you like? What would you change?"),
        required=False,
        widget=forms.Textarea)

    more = forms.CharField(
        label=_("Do you want to tell us something else?"),
        required=False,
        widget=forms.Textarea)

    ideas = forms.CharField(
        label=_("Do you have some Ideas what we could implement in AlekSIS?"),
        required=False,
        widget=forms.Textarea)


class REBUSForm(forms.Form):
    selects = []
    for select in REBUSSelectModel.objects.filter(toplevel=True):
        choices = []

        for s in select.children:
            choices.append(s.name)

        choice_field = forms.ChoiceField(
            label=_(select.name),
            widget=Select2Widget(),
            choices=choices,
        )

    short_description = forms.CharField(label=_("Please describe the error in one sentence."), required=True)
    long_description = forms.CharField(widget=forms.Textarea, label=_("Please describe the error more detailed."),
                                       required=False)
