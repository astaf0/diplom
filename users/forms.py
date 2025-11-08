from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate
from phonenumber_field.formfields import PhoneNumberField

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Пароль')
    password2 = forms.CharField(label='Подтвердите пароль')

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return email

    def clean(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email')
    password = forms.CharField(label='Пароль')

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if email and password:
            self.user_cache = authenticate(
                self.request,
                username=email,
                password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError("Неверный email или пароль")
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data


class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='Email')
    username = forms.CharField(label='Имя пользователя')
    phone = PhoneNumberField(
        label='Телефон',
        required=False,
        region='RU',
        widget=forms.TextInput(attrs={
            'placeholder': '+7 999 999 99 99',
        })
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'phone']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email