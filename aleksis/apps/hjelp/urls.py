from django.urls import path

from . import views

urlpatterns = [
    path("rebus/", views.rebus, name="rebus"),
    path("feedback/", views.feedback, name="feedback"),
    path("faq/", views.faq, name="faq"),
    path("faq/ask/", views.ask, name="ask-faq"),
    path("ajax/rebus_get_icon/", views.rebus_get_icon, name="rebus-get-icon"),
]
