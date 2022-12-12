from wtforms import Form,StringField,TextAreaField,PasswordField,SubmitField,validators,ValidationError
from flask_wtf.file import FileRequired,FileAllowed,FileField
from flask_wtf import FlaskForm
from .model import Register

class CustomerRegisterForm(FlaskForm):
    name = StringField('姓名:')
    username = StringField('用户名: ',[validators.DataRequired()])
    email = StringField('电子邮件地址: ',[validators.Email(),validators.DataRequired()])
    password = PasswordField('密码: ',[validators.DataRequired(),validators.EqualTo('confirm',
    message='两次输入密码必须一致！')])
    confirm = PasswordField('重复密码: ',[validators.DataRequired()])
    country = StringField('国家: ',[validators.DataRequired()])
    state = StringField('省份: ',[validators.DataRequired()])
    city = StringField('城市: ',[validators.DataRequired()])
    contact = StringField('电话: ',[validators.DataRequired()])
    address = StringField('地址: ',[validators.DataRequired()])
    zipcode = StringField('邮政编码: ',[validators.DataRequired()])

    profile = FileField('头像',validators=[FileAllowed(['jpg','png','jpeg','gif'],'Image only please')])

    submit = SubmitField('注册')

    def validate_username(self,username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError("用户名已经被使用！") 

    def validate_email(self,email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError("电子邮件地址已经被使用！")

class CustomerLoginForm(FlaskForm):
    email = StringField('电子邮件地址: ',[validators.Email(),validators.DataRequired()])
    password = PasswordField('密码: ',[validators.DataRequired()])