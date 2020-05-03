from django import forms
from django.utils.translation import gettext_lazy as _

from dynamic_preferences.types import StringPreference
from dynamic_preferences.preferences import Section

from aleksis.core.registries import site_preferences_registry
from aleksis.core.settings import ADMINS as admins


hjelp = Section("hjelp")


@site_preferences_registry.register
class FAQRecipient(StringPreference):
    field_class = forms.EmailField
    section = hjelp
    name = "faq_recipient"
    default = admins[0].email
    required = False
    verbose_name = _("Recipient e-mail address for FAQ questions")


@site_preferences_registry.register
class IssueReportRecipient(StringPreference):
    field_class = forms.EmailField
    section = hjelp
    name = "issue_report_recipient"
    default = admins[0].email
    required = False
    verbose_name = _("Recipient e-mail address for issue reports")


@site_preferences_registry.register
class FeedbackRecipient(StringPreference):
    field_class = forms.EmailField
    section = hjelp
    name = "feedback_recipient"
    default = admins[0].email
    required = False
    verbose_name = _("Recipient e-mail address for feedback")
