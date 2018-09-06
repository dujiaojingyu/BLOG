from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名',widget=forms.TextInput(
                                attrs={'class':'form-control','placeholder':'请输入用户名'}))
    password = forms.CharField(label='密码',widget=forms.PasswordInput(
                                attrs={'class':'form-control','placeholder':'请输入密码'}))

    #在forms表单里验证用户名和密码是否正确
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)#验证用户名和密码是否在数据库中，存在返回用户名，不存在返回空
        #如果user为空
        if user is None:
            #触发错误
            raise forms.ValidationError('用户名或密码错误')
        else:
            #否则将用户名放入cleaned_data中
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegisterForm(forms.Form):

    username = forms.CharField( max_length=30,
                                min_length=3,
                                label='用户名',widget=forms.TextInput(
                                attrs={'class':'form-control','placeholder':'请输入3-30位用户名'}))
    email =forms.EmailField(
                            label="邮箱", widget=forms.EmailInput(
                            attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}))

    password = forms.CharField( min_length=8,
                                max_length=18,
                                label='密码',widget=forms.PasswordInput(
                                attrs={'class':'form-control','placeholder':'请输入8-18位密码'}))
    password2 = forms.CharField(min_length=8,
                                max_length=18,
                                label='确认密码', widget=forms.PasswordInput(
                                attrs={'class': 'form-control', 'placeholder': '请再次输入8-18位密码'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']

        if password != password2:
            raise forms.ValidationError('两次密码不一致')
        return password2