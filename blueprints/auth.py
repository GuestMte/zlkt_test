from flask import Blueprint,render_template,jsonify,redirect,url_for,session
from exts import mail,db
from flask_mail import Message
from flask import request
import string
import random
from models import EmailCaptchaModel
from .forms import RegisterForm,LoginForm
from models import UserModel
from werkzeug.security import generate_password_hash,check_password_hash



bp=Blueprint("auth",__name__,url_prefix="/auth")#设置前缀

#/auth/login
@bp.route("/login",methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template("login.html")
    else:
        form=LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user=UserModel.query.filter_by(email=email).first()
            if not user:
                print("邮箱在数据库中不存在")
                return redirect(url_for("auth.login"))
            if check_password_hash(user.password,password):
                #cookie和session
                #cookie不适合存储太多的数据，只适合存储少量的数据
                #cookie一般用来存放登录授权的东西
                #flask中的session是经过加密后存储在cookie中的
                session['user_id']=user.id
                return redirect("/")
            else:
                print("密码错误")
                return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.login"))


@bp.route("/register",methods=['GET','POST'])#支持GET和POST请求
def register():
    if request.method=='GET':
        return render_template("register.html")
    else:
        # 验证用户提交的邮箱和验证码是否对应且正确
        # 表单验证：flask-wtf:wtforms
        form=RegisterForm(request.form)
        if form.validate():#自动调用验证器
            email=form.email.data
            username=form.username.data
            password=form.password.data
            user=UserModel(email=email,usename=username,password=generate_password_hash(password))#密码加密后存储进去
            db.session.add(user)
            db.session.commit()
            #return redirect("/auth/login")
            return redirect(url_for("auth.login"))#注册成功后 重定向
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))

#退出登录
@bp.route("/logout")
def logout():
    session.clear()#删除所有session信息
    return redirect("/")


#如果不指定method，默认是get
@bp.route("/captcha/email")
def get_email_captcha():
    email=request.args.get(("email"))
    #验证码
    #string.digits*4 0123456789012345678901234567890123456789
    source=string.digits+string.ascii_letters#数字加大小26字母
    source=source * 4
    captacha=random.sample(source,6)#返回一个列表
    #列表变成字符串
    captacha="".join(captacha)
    #I/O操作比较耗时，一般放入队列任务去做，异步
    message = Message(subject="验证码", recipients=[email], body=f"您的验证码是:{captacha},请不要告诉别人")
    mail.send(message)
    # print(captacha)
    #memcached redis 两种缓存机制，后者功能更全
    #这里用数据库的方式去存储,不过这的存储和提取数据较慢
    email_capture=EmailCaptchaModel(email=email,captcha=captacha)
    db.session.add(email_capture)
    db.session.commit()
    #RESTful API
    return jsonify({"code":200,"message":"","data":None})



@bp.route("/mail/test")
def mail_test():
    message =Message(subject="邮箱测试",recipients=["1282297618@qq.com"],body="hello，你好呀")
    mail.send(message)
    return "邮件发送成功"
