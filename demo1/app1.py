from flask import Flask, render_template,flash
from datetime import datetime
from demo1 import config
import locale

#app = Flask(__name__,template_folder=r"E:\flask\demo4")#自定义templates路径,static_folder可以自定义静态文件路径
app = Flask(__name__)
app.config.from_object(config)
app.config['SECRET_KEY']="123485sda"

class User:
    def __init__(self,username,email):
        self.username=username
        self.email=email


#print(app.config["TOKEN_KEY"])
@app.route('/')
def index():
    return render_template("demo1/index.html")



@app.route('/variable')
def variable():
    person={
        "name":"张三",
        "age":18
    }
    user=User("李四","xx@qq.com")
    hobby="游戏"
    contex={
        "hobby1":hobby,
        "person":person,
        "user":user
    }

    #return render_template("variable.html",hobby1=hobby,person=person,user=user)
    return render_template("demo1/variable.html", **contex)#变量比较多时可以使用这个方法

#两种定义过滤器方式
# #自定义过滤器格式,时间格式化
# def datetime_format(value,format="%Y年%m%d %H:%M"):
#     return value.strftime(format)
# app.add_template_filter(datetime_format,"dformat")#注册过滤器,第一个参数是函数，第二个参数是过滤器名称
locale.setlocale(locale.LC_CTYPE, 'Chinese')#设置为中文
@app.template_filter("dformat")
def datetime_format(value,format="%Y年%m月%d日 %H:%M"):
    return value.strftime(format)


@app.route("/filter")
def filter_demo():
    user = User("李四sads", "xx@qq.com")
    mytime=datetime.now()
    return render_template("demo1/filter.html", user=user, mytime=mytime)

@app.route("/control")
def control_statement():
    books=[{
        "name":"三国演员",
        "author":"罗贯中",
        "age":100
    },{
        "name":"水浒传",
        "author":"施耐庵",
        "age":19
    },{
        "name":"红楼梦",
        "author":"曹雪芹",
        "age":26
    },{
        "name":"西游记",
        "author":"吴承恩",
        "age":10
    }



    ]
    age=16
    return render_template("demo1/control.html", age=age, books=books)


@app.route("/flash")
def myflash():
    flash("我是消息内容1……")
    flash("我是消息内容2……")
    return  render_template("demo1/flash.html")

@app.route("/child1")
def child1():
    return render_template("demo1/child1.html")

@app.route("/child2")
def child2():
    return render_template("demo1/child2.html")


@app.route("/static")
def static_demo():
    return render_template("demo1/static.html")







