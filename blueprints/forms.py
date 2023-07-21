import wtforms
from wtforms.validators import Email,Length,EqualTo,InputRequired
from models import UserModel,EmailCaptchaModel
from exts import db

#验证前端提交的数据是否符合要求
class RegisterForm(wtforms.Form):
    email=wtforms.StringField(validators=[Email(message="邮箱格式错误！")])#验证邮箱格式
    captcha=wtforms.StringField(validators=[Length(min=6,max=6,message="验证码格式错误！")])
    username=wtforms.StringField(validators=[Length(min=3,max=20,message="用户名格式错误！")])
    password=wtforms.StringField(validators=[Length(min=6,max=20,message="密码格式错误")])
    password_confirm=wtforms.StringField(validators=[EqualTo("password",message="两次密码不一致")],)#验证密码是否相等

    #自定义验证：
    #1.邮箱是否已经被注册

    def validate_email(self,field):
       email=field.data
       user=UserModel.query.filter_by(email=email).first()
       if user:
           raise wtforms.ValidationError(message="该邮箱已经被注册")

    # 2.验证码是否正确
    def validate_captcha(self,field):
        captcha=field.data#field默认是代表_captcha 下划线后面的变量
        email=self.email.data
        captcha_model=EmailCaptchaModel.query.filter_by(email=email,captcha=captcha).first
        if not captcha_model:
            raise wtforms.ValidationError(message="邮箱或者验证码错误")
        # #验证完，可以删除captcha_model,不过这样的话，数据库操作可能太频繁，消耗性能
        # else:
        #     db.session.delete(captcha_model)
        #     db.session.commit()



class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])  # 验证邮箱格式
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误")])

class QuestionForm(wtforms.Form):
    title=wtforms.StringField(validators=[Length(min=3,max=100,message="标题格式错误")])
    content=wtforms.StringField(validators=[Length(min=3,message="内容格式错误")])

class AnswerForm(wtforms.Form):
    content=wtforms.StringField(validators=[Length(min=3,message="内容格式错误")])
    question_id=wtforms.StringField(validators=[InputRequired(message="必须要传入问题ig!")])
