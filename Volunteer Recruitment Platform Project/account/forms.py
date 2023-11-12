from django import forms

from .models import Institute, Volunteergroup


class LoginForm(forms.Form):
    username = forms.CharField(label="志愿者编号", max_length=10, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "UserID", 'autofocus': ''}),
                             error_messages={'required': '用户名不能为空', 'max_length': '用户名最不超过为10个字符'}, )
    password = forms.CharField(label="密码", max_length=20,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))


class RegisterForm(forms.Form):
    username = forms.CharField(label="志愿者姓名", max_length=10, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "UserID", 'autofocus': ''}))
    password1 = forms.CharField(label="密码", max_length=20,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))
    password2 = forms.CharField(label="确认密码", max_length=20,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))
    institute = forms.ModelChoiceField(queryset=Institute.objects.all(), required=True)
    volunteergroup = forms.ModelChoiceField(queryset=Volunteergroup.objects.all(), required=True)
    # institute = forms.CharField(label="学院", max_length=20, widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder': "UserID", 'autofocus': ''}))
    # volunteergroup = forms.CharField(label="义工组织", max_length=20, widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder': "UserID", 'autofocus': ''}))
