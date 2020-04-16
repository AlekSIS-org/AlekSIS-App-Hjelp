from django.db import models

from django.utils.translation import ugettext_lazy as _

from aleksis.core.mixins import ExtensibleModel

from .model_helper import COLORS, ICONS

from ckeditor.fields import RichTextField


class Support(ExtensibleModel):
    class Meta:
        permissions = (
            ("use_rebus", _("Can use REBUS")),
            ("send_feedback", _("Can send feedback"))
        )


class FAQSection(ExtensibleModel):
    name = models.CharField(max_length=200, verbose_name=_("Name"))

    icon = models.CharField(max_length=50, blank=True, default="question_answer", choices=ICONS,
                            verbose_name=_("Symbol"))
    icon_color = models.CharField(max_length=20, default="black", choices=COLORS, verbose_name=_("Symbol colour"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("FAQ section")
        verbose_name_plural = _("FAQ sections")


class FAQQuestion(ExtensibleModel):
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


class REBUSCategory(ExtensibleModel):
    name = models.CharField(max_length=40, verbose_name=_("Category name"))
    icon = models.CharField(max_length=50, blank=True, default="bug_report", choices=ICONS,
                            verbose_name=_("Symbol"))
    parent = models.ForeignKey("self", related_name="children", on_delete=models.CASCADE, blank=True,
                               null=True, verbose_name=_("Parent"))
    free_text = models.BooleanField(verbose_name=_("Free text input allowed"), default=False)
    placeholder = models.CharField(max_length=100, verbose_name=_("Placeholder"), blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.free_text:
            REBUSCategory.objects.filter(parent=self).delete()
        super(REBUSCategory, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Bug report category")
        verbose_name_plural = _("Bug report categories")
