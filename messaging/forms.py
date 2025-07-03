from django import forms
from .models import Mailing, Message


class MailingForm(forms.ModelForm):
    new_message = forms.CharField(
        widget=forms.Textarea(attrs={'rows':4}),
        label='Текст сообщения',
        required=False  # Или True, если обязательно
    )

    class Meta:
        model = Mailing
        fields = ['start_time', 'end_time', 'status', 'clients', 'message']

    def save(self, commit=True):
        mailing = super().save(commit=False)
        message_text = self.cleaned_data.get('new_message', '')

        if hasattr(self.instance, 'message') and self.instance.message:
            self.instance.message.body = message_text
            self.instance.message.save()
        else:
            message = Message.objects.create(
                body=message_text,
            )
            mailing.message = message
        if commit:
            mailing.save()
        return mailing



class MessageForm(forms.ModelForm):
    body = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Введите текст сообщения',
            'rows': 5,
            'class': 'form-control',
            'maxlength': '250'
        }),
        help_text="Максимум 250 символов",
        label="Текст сообщения"
    )

    class Meta:
        model = Message
        fields = ['subject', 'body']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите тему сообщения'
            }),
        }
        labels = {
            'subject': 'Тема сообщения',
        }
        help_texts = {
            'subject': 'Кратко опишите сообщение',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if 'class' not in self.fields[field].widget.attrs:
                self.fields[field].widget.attrs['class'] = 'form-control'
