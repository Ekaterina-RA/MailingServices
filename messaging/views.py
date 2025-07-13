from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    RedirectView, TemplateView,
)
from messaging.forms import ClientForm, MessageForm, MailingForm
from messaging.mixins import OwnerRequiredMixin
from messaging.models import Client, Message, Mailing, Attempt
from django.contrib import messages
from users.models import User


class MessagingHomeView(TemplateView):
    template_name = 'messaging/home.html'
    context_object_name = "home"

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "messaging/client_list.html"
    context_object_name = "clients"

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "messaging/client_form.html"
    success_url = reverse_lazy("messaging:client_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "messaging/client_form.html"
    success_url = reverse_lazy("messaging:client_list")

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = "messaging/client_confirm_delete.html"
    success_url = reverse_lazy("messaging:client_list")

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "messaging/message_list.html"

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "messaging/message_form.html"
    success_url = reverse_lazy("messaging:message_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(OwnerRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "messaging/message_form.html"
    success_url = reverse_lazy("messaging:message_list")

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDeleteView(OwnerRequiredMixin, DeleteView):
    model = Message
    template_name = "messaging/message_confirm_delete.html"
    success_url = reverse_lazy("messaging:message_list")

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "messaging/message_detail.html"

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "messaging/mailing_list.html"
    context_object_name = "mailings"

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


def mailing_list(request):
    return render(request, 'messaging/mailing_list.html')


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "messaging/mailing_form.html"
    success_url = reverse_lazy("messaging:mailing_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        print(f"Created mailing with ID: {self.object.id}")
        return response

    def form_invalid(self, form):
        print("Form errors:", form.errors)
        return super().form_invalid(form)

    def create_mailing(request):
        if request.method == "POST":
            form = MailingForm(request.POST, user=request.user)
            if form.is_valid():
                mailing = form.save(commit=False)
                mailing.owner = request.user
                mailing.save()
                form.save_m2m()  # Важно для ManyToMany!
                return redirect("mailing_list")
        else:
            form = MailingForm(user=request.user)
        return render(request, "messaging/mailing_form.html", {"form": form})


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "messaging/mailing_form.html"
    success_url = reverse_lazy("messaging:mailing_list")

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "messaging/mailing_confirm_delete.html"
    success_url = reverse_lazy("messaging:mailing_list")

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "messaging/mailing_detail.html"
    context_object_name = "mailing"

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingSendView(LoginRequiredMixin, View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk, owner=request.user)
        try:
            sent_count = mailing.send()
            Attempt.objects.create(
                mailing=mailing, status="SUCCESS", server_response="Успешно"
            )
            messages.success(
                request, f"Рассылка успешно отправлена {sent_count} клиентам!"
            )
        except Exception as e:
            Attempt.objects.create(
                mailing=mailing, status="FAILURE", server_response={str(e)}
            )
            messages.error(request, f"Ошибка при отправке рассылки: {str(e)}")
        return redirect("messaging:mailing_list")


class UserMailingsView(PermissionRequiredMixin, ListView):
    permission_required = "messaging.can_view_all_mailings"
    template_name = "messaging/user_mailings.html"
    context_object_name = "mailings"

    def dispatch(self, request, *args, **kwargs):
        self.target_user = get_object_or_404(User, pk=self.kwargs["user_id"])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.target_user).select_related("message")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["target_user"] = self.target_user
        return context


class UserListView(PermissionRequiredMixin, ListView):
    permission_required = "users.view_user"
    template_name = "messaging/user_list.html"
    context_object_name = "users"
    queryset = User.objects.all().select_related("profile").order_by("-date_joined")


def block_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = False
    user.save()
    return redirect("messaging:users_list")


def disable_mailing(request, mailing_id):
    mailing = get_object_or_404(Mailing, pk=mailing_id)
    mailing.is_active = False  # отключить рассылку (флаг)
    mailing.status = Mailing.FAILED  # или другой статус по вашему выбору
    mailing.save()
    return redirect("messaging:mailings_list")


class AttemptListView(LoginRequiredMixin, ListView):
    model = Attempt
    template_name = "attempts/attempt_list.html"
    context_object_name = "attempts"

    def get_queryset(self):
        return Attempt.objects.filter(mailing__owner=self.request.user)


@login_required
@permission_required("messaging.change_mailing")
def disable_mailing(request, mailing_id):
    mailing = get_object_or_404(Mailing, pk=mailing_id)
    mailing.is_active = False
    mailing.status = Mailing.COMPLETED
    mailing.save()
    return redirect("messaging:mailing_list")


class DisableMailingView(View):
    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing.is_active = False
        mailing.save()
        return redirect('messaging:mailing_list')