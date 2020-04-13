from django.contrib import admin
from .models import FAQQuestion, FAQSection, REBUSCategory
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _


def show(modeladmin, request, queryset):
    queryset.update(show=True)


show.short_description = _("Publish selected questions")


def hide(modeladmin, request, queryset):
    queryset.update(show=False)


hide.short_description = _("Unpublish selected questions")


class FAQSectionAdmin(admin.ModelAdmin):
    list_display = ("name", "_icon")

    class Media:
        css = {
            'all': ('/static/css/materialdesignicons-webfont/material-icons.css',)
        }

    def _icon(self, obj):
        return format_html(u'<i style="color: {};" class="material-icons">{}<i/>', obj.icon_color, obj.icon)


class FAQQuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "section", "_icon", "show")
    actions = [show, hide]

    class Media:
        css = {
            'all': ('/static/css/materialdesignicons-webfont/material-icons.css',)
        }

    def _icon(self, obj):
        return format_html(u'<i class="material-icons">{}<i/>', obj.icon)


class REBUSCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "_icon", "_parent", "_placeholder", "_tagging")

    class Media:
        css = {
            'all': ('/static/css/materialdesignicons-webfont/material-icons.css',)
        }

    def _icon(self, obj):
        return format_html(u'<i class="material-icons">{}<i/>', obj.icon)

    def _parent(self, obj):
        return obj.parent

    def _placeholder(self, obj):
        return obj.placeholder

    def _tagging(self, obj):
        return obj.tagging


admin.site.register(FAQQuestion, FAQQuestionAdmin)
admin.site.register(FAQSection, FAQSectionAdmin)
admin.site.register(REBUSCategory, REBUSCategoryAdmin)
