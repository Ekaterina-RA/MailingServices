from django.contrib.auth import logout
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetConfirmView,
)
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView, View
from .forms import RegisterForm, CustomPasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib import messages
from users.mixins import ManagerRequiredMixin, UserAccessMixin
from messaging.models import Mailing


class CustomLoginView(LoginView):
    template_name = "auth/login.html"

    def form_valid(self, form):
        user = form.get_user()
        if user.is_blocked:
            messages.error(self.request, "Ваш аккаунт заблокирован")
            return redirect("login")
        return super().form_valid(form)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "auth/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, "Регистрация прошла успешно!")
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)  # Логируем ошибки
        return super().form_invalid(form)


def custom_logout(request):
    logout(request)
    return redirect("home")


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = "auth/password_reset.html"
    email_template_name = "auth/password_reset_email.html"
    success_url = reverse_lazy("users:login")


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "auth/password_reset_confirm.html"
    success_url = reverse_lazy("users:login")


def activate_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.email_confirmed = True
        user.save()
        messages.success(request, "Email успешно подтвержден!")
        return redirect("users:login")
    else:
        messages.error(request, "Ссылка подтверждения недействительна!")
        return redirect("home")


class StatsView(ManagerRequiredMixin, TemplateView):
    template_name = "stats/user_stats.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stats, created = UserStats.objects.get_or_create(user=self.request.user)
        stats.update_stats()

        context.update(
            {
                "stats": stats,
                "mailings": Mailing.objects.filter(owner=self.request.user),
                "attempts": MailingAttempt.objects.filter(
                    mailing__owner=self.request.user
                )[:10],
            }
        )
        return context


class MailingListView(UserAccessMixin, ListView):
    model = Mailing
    template_name = "messaging/mailing_list.html"
    context_object_name = "mailings"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role == "manager":
            context["users"] = User.objects.all()
        return context


class BlockUserView(ManagerRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.is_blocked = not user.is_blocked
        user.save()
        return redirect("mailing_list")


class DisableMailingView(ManagerRequiredMixin, View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing.status = "completed"
        mailing.save()
        return redirect("mailing_list")
