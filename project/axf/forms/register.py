from django import forms


#  define register forms Class here


class RegisterForm(forms.Form):
    '''required=True表示必填; 文本输入TextInput和Textarea可以实现相同的功能;
    # 其中attrs为指定对应字段的前端样式，相当于html表单中的class指定样式'''
    # 注意attrs样式中的name一定是下面的变量命名，重新在attrs中对name命名是无效的
    username = forms.CharField(max_length=12, min_length=6, required=True,
                               error_messages={"required": "账号不能为空", "invalid": "格式错误"},
                               widget=forms.PasswordInput(attrs={"id": "account", "type": "text",
                                                                 "class": "form-control",
                                                                 "placeholder": "账号长度为6到12个字符",
                                                                 "aria-describedby": "basic-addon1", }))
                                                        # "name": "userAccount"})) # 在这里定义的name无效，name仍会是username

    password = forms.CharField(max_length=16, min_length=6, required=True,
                               widget=forms.PasswordInput(attrs={"id": "pass", "type": "password",
                                                                 "class": "form-control",
                                                                 "placeholder": "密码长度为6~16个字符",
                                                                 "aria-describedby": "basic-addon1",}))

    password_confirm = forms.CharField(max_length=16, min_length=6, required=True,
                                       widget=forms.PasswordInput(attrs={"id": "password", "type": "password",
                                                                         "class": "form-control",
                                                                         "placeholder": "密码长度为6~16个字符",
                                                                         "aria-describedby": "basic-addon1",}))
    # ...其他注册栏位可根据实际需求再添加
