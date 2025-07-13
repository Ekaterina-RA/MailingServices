from django.urls import path
from . import views
from .apps import MessagingConfig
from .views import ClientCreateView, AttemptListView, MessageDeleteView, MessageDetailView, \
    MessageCreateView, ClientListView, MailingSendView, MailingCreateView, MailingDetailView, MailingListView, \
    MessagingHomeView, DisableMailingView, MessageUpdateView, MessageListView, MailingDeleteView

app_name = MessagingConfig.name

urlpatterns = [
    # Mailing URLs
    path("mailings/", MailingListView.as_view(), name="mailing_list"),
    path("mailings/create/", MailingCreateView.as_view(), name="mailing_create"),
    path(
        "mailings/<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"
    ),
    path(
        "mailings/<int:pk>/update/",
        views.MailingUpdateView.as_view(),
        name="mailing_update",
    ),
    path(
        "mailings/<int:pk>/delete/",
        MailingDeleteView.as_view(),
        name="mailing_delete",
    ),
    path(
        "mailings/<int:pk>/send/", MailingSendView.as_view(), name="mailing_send"),
    path('mailings/<int:pk>/disable/', DisableMailingView.as_view(), name='disable_mailing'),

    # Client URLs
    path("clients/", ClientListView.as_view(), name="client_list"),
    path("clients/create/", ClientCreateView.as_view(), name="client_create"),
    path(
        "clients/<int:pk>/update/",
        views.ClientUpdateView.as_view(),
        name="client_update",
    ),
    path(
        "clients/<int:pk>/delete/",
        views.ClientDeleteView.as_view(),
        name="client_delete",
    ),

    path("messages/", MessageListView.as_view(), name="message_list"),
    path("messages/create/", MessageCreateView.as_view(), name="message_create"),
    path(
        "messages/<int:pk>/", MessageDetailView.as_view(), name="message_detail"
    ),
    path(
        "messages/<int:pk>/update/",
        MessageUpdateView.as_view(),
        name="message_update",
    ),
    path(
        "messages/<int:pk>/delete/",
        MessageDeleteView.as_view(),
        name="message_delete",
    ),
    path("attempts/",AttemptListView.as_view(), name="attempt_list"),
    path("", MessagingHomeView.as_view(), name="home"),
]

