from django.urls import path

from . import views

urlpatterns = [
    path("rebus/", views.rebus, name="rebus"),
    path("feedback/", views.feedback, name="feedback"),
    path('', views.faq, name='faq'),
    path('ask/', views.ask, name='ask-faq')
]
