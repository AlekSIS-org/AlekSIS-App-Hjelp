from django import forms
from django.utils.translation import ugettext_lazy as _


class FAQForm(forms.Form):
    question = forms.CharField(widget=forms.Textarea(),
                               label='Deine Frage', required=True)


class REBUSForm(forms.Form):
    a = forms.CharField(label=_("Category A"), required=True)
    b = forms.CharField(label=_("Category B"), required=False)
    c = forms.CharField(label=_("Category C"), required=False)
    short_description = forms.CharField(label=_("Bitte beschreiben Sie Ihren Fehler in einem Satz"), required=True)
    long_description = forms.CharField(widget=forms.Textarea, label=_("Bitte beschreiben Sie Ihren Fehler genauer"),
                                       required=False)


class FeedbackForm(forms.Form):
    ratings = [(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)]

    design_rating = forms.ChoiceField(label=_("Design der Oberfläche"),
                                      choices=ratings,
                                      widget=forms.RadioSelect(attrs={"checked": "checked"}),
                                      required=True,
                                      )

    performance_rating = forms.ChoiceField(label=_("Geschwindigkeit"),
                                           choices=ratings,
                                           widget=forms.RadioSelect(attrs={"checked": "checked", "class": "required"}),
                                           required=True)

    usability_rating = forms.ChoiceField(label=_("Benutzerfreundlichkeit"),
                                         choices=ratings,
                                         widget=forms.RadioSelect(attrs={"checked": "checked"}),
                                         required=True)

    overall_rating = forms.ChoiceField(label=_("SchoolApps allgemein"),
                                       choices=ratings,
                                       widget=forms.RadioSelect(attrs={"checked": "checked"}),
                                       required=True)

    apps = forms.CharField(
        label=_("Was gefällt Dir an SchoolApps? Was würdest du ändern?"),
        required=False,
        widget=forms.Textarea)

    more = forms.CharField(
        label=_("Möchtest Du uns sonst noch etwas mitteilen?"),
        required=False,
        widget=forms.Textarea)

    ideas = forms.CharField(
        label=_("Hast Du Ideen, was wir noch in SchoolApps einbauen sollten?"),
        required=False,
        widget=forms.Textarea)
