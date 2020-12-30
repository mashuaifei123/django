#forms.py
 
from django import forms
from django.forms import widgets
 
class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100,
                               error_messages={"min_length":"最短为5个字符","required":"该字段不能为空"},
                               label='用户名',
                               widget=widgets.TextInput(attrs={"placeholder":"请输入用户名成"})
                               )
    password = forms.CharField(max_length=100,
                               widget=widgets.PasswordInput(attrs={"placeholder":"password"})
                                )

    telephone=forms.IntegerField(error_messages={"invalid":"格式错误"})

    gender=forms.CharField(
          initial=2,
          widget=widgets.Select(choices=((1,'上海'),(2,'北京'),))
             )

    email = forms.EmailField()
    is_married = forms.BooleanField(required=False)