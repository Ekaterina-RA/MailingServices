from django.urls import path
from messaging.apps import MessagingConfig
from messaging.views import (
    ClientListView,
    ClientCreateView,
    ClientUpdateView,
    ClientDeleteView,
    MessageListView,
    MessageCreateView,
    MessageUpdateView,
    MessageDeleteView,
    MailingListView,
    MailingCreateView,
    MailingUpdateView,
    MailingDeleteView,
    MailingDetailView,
    AttemptListView,
    MessageDetailView,
    MailingSendView,
    UserMailingsView,
    UserListView,
)
from users.views import ToggleUserStatusView

app_name = MessagingConfig.name


urlpatterns = [
    # Клиенты
    path("clients/", ClientListView.as_view(), name="client_list"),
    path("clients/create/", ClientCreateView.as_view(), name="client_create"),
    path("messages/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("clients/<int:pk>/update/", ClientUpdateView.as_view(), name="client_update"),
    path("clients/<int:pk>/delete/", ClientDeleteView.as_view(), name="client_delete"),
    # Сообщения
    path("messages/", MessageListView.as_view(), name="message_list"),
    path("messages/create/", MessageCreateView.as_view(), name="message_create"),
    path(
        "messages/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"
    ),
    path(
        "messages/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"
    ),
    # Рассылки
    path("", MailingListView.as_view(), name="mailing_list"),
    path("create/", MailingCreateView.as_view(), name="mailing_create"),
    path("<int:pk>/update/", MailingUpdateView.as_view(), name="mailing_update"),
    path("<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"),
    path("<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"),
    path("mailing/<int:pk>/send/", MailingSendView.as_view(), name="mailing_send"),
    path(
        "users/<int:user_id>/mailings/",
        UserMailingsView.as_view(),
        name="user_mailings",
    ),
    path("users/", UserListView.as_view(), name="user_list"),
    path("users/toggle-status/<int:pk>/", ToggleUserStatusView.as_view(), name="toggle_user_status"),

    # Попытки рассылки
    path("attempts/", AttemptListView.as_view(), name="attempt_list"),
]
