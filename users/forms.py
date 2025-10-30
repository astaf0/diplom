from django import forms
from django.contrib.auth import authenticate, get_user_model

class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].help_text = None
            self.fields[field_name].widget.attrs.update({
                'autocomplete': 'off',
            })

    def clean(self):
        data = self.cleaned_data
        username = data['username']
        password = data['password']
        self.user = authenticate(self.request, username=username, password=password)
        if not self.user:
            raise forms.ValidationError('Неверное имя пользователя или пароль')
        return data

    def get_user(self):
        return self.user


class RegisterForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Повторите пароль')

    def clean_username(self):
        username = self.cleaned_data['username']
        User = get_user_model()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким именем уже есть')
        return username

    def clean(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data