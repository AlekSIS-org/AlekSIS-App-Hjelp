from rules import add_perm, always_allow

from aleksis.core.util.predicates import (
    has_global_perm,
    has_person,
)

# Ask FAQ question
ask_faq_predicate = has_person & has_global_perm("hjelp.ask_faq")
add_perm("hjelp.ask_faq", ask_faq_predicate)

# Report issue
report_issue_predicate = has_person & has_global_perm("hjelp.report_issue")
add_perm("hjelp.report_issue", report_issue_predicate)

# Add feedback
send_feedback_predicate = has_person & has_global_perm("hjelp.send_feedback")
add_perm("hjelp.send_feedback", send_feedback_predicate)
