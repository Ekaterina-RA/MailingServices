from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from messaging.forms import ClientForm, MessageForm, MailingForm
from messaging.mixins import OwnerRequiredMixin
from messaging.models import Client, Message, Mailing, Attempt


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'messaging/client_list.html'

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'messaging/client_form.html'
    success_url = reverse_lazy('messaging:client_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'messaging/client_form.html'
    success_url = reverse_lazy('messaging:client_list')

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'messaging/client_confirm_delete.html'
    success_url = reverse_lazy('messaging:client_list')

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messaging/message_list.html'

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'messaging/message_form.html'
    success_url = reverse_lazy('messaging:message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(OwnerRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'messaging/message_form.html'
    success_url = reverse_lazy('messaging:message_list')


class MessageDeleteView(OwnerRequiredMixin, DeleteView):
    model = Message
    template_name = 'messaging/message_confirm_delete.html'
    success_url = reverse_lazy('messaging:message_list')


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'messaging/message_detail.html'

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)



class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'messaging/mailing_list.html'

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'messaging/mailing_form.html'
    success_url = reverse_lazy('messaging:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'messaging/mailing_form.html'
    success_url = reverse_lazy('messaging:mailing_list')

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'messaging/mailing_confirm_delete.html'
    success_url = reverse_lazy('messaging:mailing_list')

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'messaging/mailing_detail.html'

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class AttemptListView(LoginRequiredMixin, ListView):
    model = Attempt
    template_name = 'attempts/attempt_list.html'

    def get_queryset(self):
        return Attempt.objects.filter(mailing__owner=self.request.user)