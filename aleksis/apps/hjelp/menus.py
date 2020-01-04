from django.utils.translation import ugettext_lazy as _

MENUS = {
    "NAV_MENU_CORE": [
        {
            "name": _("Support"),
            "url": "#",
            "root": True,
            "validators": [
                "menu_generator.validators.is_authenticated",
                "aleksis.core.util.core_helpers.has_person",
            ],
            "submenu": [
                {
                    "name": _("Report a Bug"),
                    "url": "rebus",
                    "validators": ["menu_generator.validators.is_authenticated"],
                },
                {
                    "name": _("Feedback"),
                    "url": "feedback",
                    "validators": ["menu_generator.validators.is_authenticated"],
                },
                {
                    "name": _("FAQ"),
                    "url": "faq",
                    "validators": ["menu_generator.validators.is_superuser"],
                },
            ],
        }
    ]
}
