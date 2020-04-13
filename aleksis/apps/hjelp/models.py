from django.db import models

from django.utils.translation import ugettext_lazy as _

from .model_helper import COLORS, ICONS

from ckeditor.fields import RichTextField


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
    answer_text = RichTextField(help_text=_("Because of our CSS framework the HTML tag "
                                            "<strong>&lt;ul&gt;</strong> must have the CSS "
                                            "class <em>browser-default</em>. In this case, please "
                                            "use the manual editor mode."))

    section = models.ForeignKey(FAQSection, on_delete=models.CASCADE, blank=True, related_name="questions",
                                verbose_name=_("Section"))

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name = _("FAQ questions")
        verbose_name_plural = _("FAQ questions")


class REBUSCategory(models.Model):
    name = models.CharField(max_length=40, verbose_name=_("Category name"))
    icon = models.CharField(max_length=50, blank=True, default="bug_report", choices=ICONS,
                            verbose_name=_("Symbol"))
    parent = models.ForeignKey("self", related_name="children", on_delete=models.CASCADE, blank=True,
                               null=True, verbose_name=_("Parent"))
    tagging = models.BooleanField(verbose_name=_("Tagging allowed"), default=False)
    placeholder = models.CharField(max_length=100, verbose_name=_("Placeholder"), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Bug report category")
        verbose_name_plural = _("Bug report categories")
