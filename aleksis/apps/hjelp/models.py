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

    icon = models.CharField(max_length=50, blank=True, default="question_answer", choices=ICONS, verbose_name=_("Symbol"))
    icon_color = models.CharField(max_length=20, default="black", choices=COLORS, verbose_name=_("Symbol colour"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("FAQ section")
        verbose_name_plural = _("FAQ sections")


class FAQQuestion(models.Model):
    question_text = models.TextField(verbose_name=_("Question"))
    icon = models.CharField(max_length=50, blank=True, default="question_answer", choices=ICONS, verbose_name=_("Symbol"))

    show = models.BooleanField(verbose_name=_("Published"), default=False)
    answer_text = models.TextField(blank=True,
                                   help_text=_("Bei den Antworten funktioniert auch HTML-Syntax!<br> Aus Gründen des "
                                             "verwendeten CSS-Frameworks muss der Tag <strong>&lt;ul&gt;</strong> die "
                                             "CSS-Klasse <em>browser-default</em> besitzen!"), verbose_name=_("Answer"))

    section = models.ForeignKey(FAQSection, on_delete=models.CASCADE, blank=True, related_name="questions",
                                verbose_name=_("Section"))

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name = _("FAQ questions")
        verbose_name_plural = _("FAQ questions")


mail_settings = MailSettings(_("Mail adresses"))
