from django import forms
from django.views.generic import (
    ListView,
    UpdateView,
    DeleteView,
    CreateView,
    DetailView,
    TemplateView,
    View,
)
from django.contrib.auth import logout
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetConfirmView,
)
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Client, Mailing, MailingAttempt, Message
from django.forms import ModelForm
from messaging.forms import MailingForm

@method_decorator(cache_page(60 * 5), name="dispatch")
class MessagingHomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_mailings"] = Mailing.objects.count()
        context["active_mailings"] = Mailing.objects.filter(status="started").count()
        context["unique_clients"] = Client.objects.distinct().count()
        return context


class ClientListView(ListView):
    model = Client
    template_name = "clients/client_list.html"
    context_object_name = "clients"
    paginate_by = 10


class ClientCreateView(CreateView):
    model = Client
    template_name = "clients/client_form.html"
    fields = ["email", "full_name", "comment"]
    success_url = reverse_lazy("messaging:client_list")


class ClientUpdateView(UpdateView):
    model = Client
    template_name = "clients/client_form.html"
    fields = ["email", "full_name", "comment"]
    success_url = reverse_lazy("messaging:client_list")


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "clients/client_confirm_delete.html"
    success_url = reverse_lazy("messaging:client_list")


class MessageListView(ListView):
    model = Message
    template_name = "messages/message_list.html"
    context_object_name = "messages"
    paginate_by = 10


class MessageCreateView(CreateView):
    model = Message
    template_name = "messages/message_form.html"
    fields = ["subject", "body"]
    success_url = reverse_lazy("messaging:message_list")


class MessageUpdateView(UpdateView):
    model = Message
    template_name = "messages/message_form.html"
    fields = ["subject", "body"]
    success_url = reverse_lazy("messaging:message_list")


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "messages/message_confirm_delete.html"
    success_url = reverse_lazy("messaging:message_list")



class MailingListView(ListView):
    model = Mailing
    template_name = "mailings/mailing_list.html"
    context_object_name = "mailings"
    paginate_by = 10


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("messaging:mailing_list")

    def form_valid(self, form):
        message_text = self.request.POST.get('new_message', '').strip()
        mailing = form.save(commit=False)
        message = Message.objects.create(
            body=message_text
        )
        mailing.message = message
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("messaging:mailing_list")


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "mailings/mailing_confirm_delete.html"
    success_url = reverse_lazy("messaging:mailing_list")


class MailingAttemptListView(ListView):
    model = MailingAttempt
    template_name = "attempts/attempt_list.html"
    context_object_name = "attempts"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        mailing_id = self.kwargs.get("mailing_id")
        if mailing_id:
            queryset = queryset.filter(mailing_id=mailing_id)
        return queryset.select_related("mailing")


class MailingAttemptDetailView(DetailView):
    model = MailingAttempt
    template_name = "attempts/attempt_detail.html"
    context_object_name = "attempt"


class StartMailingView(View):
    def post(self, request, pk):
        from mailing.models import Mailing

        mailing = Mailing.objects.get(pk=pk)

        if mailing.status in ["created", "started"]:
            mailing.status = "started"
            mailing.save()
            send_mailing(mailing)
            messages.success(request, "Рассылка успешно запущена")
        else:
            messages.error(request, "Рассылка уже завершена")

        return redirect("mailing_detail", pk=pk)
