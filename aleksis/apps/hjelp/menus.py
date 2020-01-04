from django.utils.translation import ugettext_lazy as _

MENUS = {
    "NAV_MENU_CORE": [
        {
            "name": _("Support"),
            "url": "#",
            "icon": "help_circle",
            "root": True,
            "validators": [
                "menu_generator.validators.is_authenticated",
                "aleksis.core.util.core_helpers.has_person",
            ],
            "submenu": [
                {
                    "name": _("Report a Bug"),
                    "url": "rebus",
                    "icon": "bug_report",
                    "validators": ["menu_generator.validators.is_authenticated"],
                },
                {
                    "name": _("Feedback"),
                    "url": "feedback",
                    "icon": "message_alert",
                    "validators": ["menu_generator.validators.is_authenticated"],
                },
                {
                    "name": _("FAQ"),
                    "url": "faq",
                    "icon": "question_answer",
                    "validators": ["menu_generator.validators.is_superuser"],
                },
            ],
        }
    ]
}
