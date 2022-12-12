from click import confirm
from wtforms import Form,BooleanField,StringField,PasswordField,validators

class RegistrationForm(Form):
    name = StringField('姓名',[validators.Length(min=4,max=25)])
    username = StringField('用户名',[validators.Length(min=4,max=25)])
    email = StringField('电子邮件地址',[validators.Length(min=6,max=35),validators.Email()])
    password = PasswordField('密码',[
        validators.DataRequired(),
        validators.EqualTo('confirm',message='两次输入密码必须一致。')
    ])
    confirm=PasswordField('确认密码')

class LoginForm(Form):
    email = StringField('电子邮件地址',[validators.Length(min=6,max=35),validators.Email()])
    password = PasswordField('密码',[validators.DataRequired()])