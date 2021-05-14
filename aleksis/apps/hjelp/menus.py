from django.utils.translation import gettext_lazy as _

MENUS = {
    "NAV_MENU_CORE": [
        {
            "name": _("Support"),
            "url": "#",
            "icon": "help",
            "root": True,
            "validators": [
                ("aleksis.core.util.predicates.permission_validator", "hjelp.show_menu",),
            ],
            "submenu": [
                {
                    "name": _("Report an issue"),
                    "url": "report_issue",
                    "icon": "bug_report",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "hjelp.report_issue",
                        ),
                    ],
                },
                {
                    "name": _("Give feedback"),
                    "url": "feedback",
                    "icon": "message_alert",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "hjelp.send_feedback",
                        ),
                    ],
                },
                {
                    "name": _("FAQ"),
                    "url": "faq",
                    "icon": "question_answer",
                    "validators": [
                        ("aleksis.core.util.predicates.permission_validator", "hjelp.view_faq",),
                    ],
                },
                {
                    "name": _("Manage FAQ"),
                    "url": "order_faq",
                    "icon": "low_priority",
                    "validators": [
                        ("aleksis.core.util.predicates.permission_validator", "hjelp.change_faq",),
                    ],
                },
            ],
        }
    ]
}
