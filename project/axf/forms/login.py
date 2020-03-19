from django import forms


#  define login forms Class here


class LoginForm(forms.Form):
    '''required=True表示必填, TextInput和Textarea可以实现相同的功能; attrs是啥??'''
    username = forms.CharField(max_length=12, min_length=6, required=True,
                               error_messages={"required": "账号不能为空", "invalid": "格式错误"},
                               widget=forms.TextInput(attrs={"class": "c"}))
    '''PasswordInput是密文输入'''
    password = forms.CharField(max_length=16, min_length=6, required=True,
                               widget=forms.PasswordInput)