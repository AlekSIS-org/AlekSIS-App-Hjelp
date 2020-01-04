from django.utils.translation import ugettext_lazy as _

MENUS = {
    "NAV_MENU_CORE": [
        {
            "name": _("Support"),
            "url": "#",
            "icon": "help-circle",
            "root": True,
            "validators": [
                "menu_generator.validators.is_authenticated",
                "aleksis.core.util.core_helpers.has_person",
            ],
            "submenu": [
                {
                    "name": _("Report a Bug"),
                    "url": "rebus",
                    "icon": "bug",
                    "validators": ["menu_generator.validators.is_authenticated"],
                },
                {
                    "name": _("Feedback"),
                    "url": "feedback",
                    "icon": "message-alert",
                    "validators": ["menu_generator.validators.is_authenticated"],
                },
                {
                    "name": _("FAQ"),
                    "url": "faq",
                    "icon": "frequently-asked-questions",
                    "validators": ["menu_generator.validators.is_superuser"],
                },
            ],
        }
    ]
}
