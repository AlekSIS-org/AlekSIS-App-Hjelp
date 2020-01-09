from django.db import models

from django.utils.translation import ugettext_lazy as _

from .model_helper import COLORS, ICONS


class Support(models.Model):
    class Meta:
        permissions = (
            ("use_rebus", _("Can use REBUS")),
            ("send_feedback", _("Can send feedback"))
        )


class FAQSection(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Name"))

    icon = models.CharField(max_length=50, blank=True, default="question_answer", choices=ICONS,
                            verbose_name=_("Symbol"))
    icon_color = models.CharField(max_length=20, default="black", choices=COLORS, verbose_name=_("Symbol colour"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("FAQ section")
        verbose_name_plural = _("FAQ sections")


class FAQQuestion(models.Model):
    question_text = models.TextField(verbose_name=_("Question"))
    icon = models.CharField(max_length=50, blank=True, default="question_answer", choices=ICONS,
                            verbose_name=_("Symbol"))

    show = models.BooleanField(verbose_name=_("Published"), default=False)
    answer_text = models.TextField(blank=True,
                                   help_text=_("You can use HTML syntax in the FAQ-answers!<br> Because of "
                                               "our CSS framework all <strong>&lt;ul&gt;</strong>-Elements "
                                               "must have the CSS class <em>browser-default</em>!"),
                                   verbose_name=_("Answer"))

    section = models.ForeignKey(FAQSection, on_delete=models.CASCADE, blank=True, related_name="questions",
                                verbose_name=_("Section"))

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name = _("FAQ questions")
        verbose_name_plural = _("FAQ questions")


class BugReportSelectModel(models.Model):
    name = models.CharField(max_length=40, verbose_name=_("Category name"))
    icon = models.CharField(max_length=50, verbose_name=_("Icon"), blank=True)
    parent = models.ForeignKey("self", related_name="children", on_delete=models.CASCADE)

    toplevel = models.BooleanField(verbose_name=_("Top-level select or optgroup"), null=True, blank=True)
