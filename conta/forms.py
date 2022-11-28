from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from conta.models import Conta

class RegistroForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text="Adicione um email válido")

    class Meta:
        model = Conta
        fields = ("email", "username", "password1", "password2")


class AutenticacaoForm(forms.ModelForm):
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

    class Meta:
        model = Conta
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Login ou Senha Incorreto(a)")


class AtualizaContaForm(forms.ModelForm):
    class Meta:
        model = Conta
        fields = ('email', 'username')

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            #agora, verificaremos se o email existe e se encontra no BD
            try:
                conta = Conta.objects.exclude(pk=self.instance.pk).get(email=email)
            except Conta.DoesNotExist:
                return email
            raise forms.ValidationError("Email %s já está em uso." %email)

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            #agora, verificaremos se o username existe e se encontra no BD
            try:
                conta = Conta.objects.exclude(pk=self.instance.pk).get(username=username)
            except Conta.DoesNotExist:
                return username
            raise forms.ValidationError("Username %s já está em uso." %username)