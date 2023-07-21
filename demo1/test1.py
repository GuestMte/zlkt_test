from flask import Flask,request,url_for,redirect
from demo1 import config

app = Flask(__name__)
app.config.from_object(config)#config.py里面的

#print(app.config["TOKEN_KEY"])
@app.route('/')
def hello_world():
    return 'Hello Flask!'

#重定向，方法1
@app.route('/login')
def login():
    return 'login page'

@app.route('/profile1')
def profile1():
    name=request.args.get('name')
    url = url_for("login", user="admin")#动态规划url
    if not name:
        #如果没有name，说明没有登录，重定向到登录页面
        return redirect(url)#重定向，给的是url
    else:
        return name


#重定向，方法2
@app.route('/blog/<int:blog_id>')# 定义参数类型
def bolg_detail(blog_id):
    return "恁查找的博客id为:%s"%blog_id

@app.route('/urlfor')# 定义参数类型
def get_url_for():
    url=url_for("bolg_detail",blog_id=2,user="admin")
    return url





@app.route('/profile')
def profile():
    return 'Hello World!'

@app.route('/blog/list/<any(python1,flask2,django3):category>')#指定范围内字符串
def bolg_list_with_category(category):
    return "您获取的博客分类为:%s"%category

@app.route('/book/list')
def book_list():
    return "我是博"

@app.route('/blog/list/<int:user_id>')#用来定义默认值
@app.route('/blog/list/<int:user_id>/<int:page>')#指定范围内字符串
def blog_list1(user_id,page=1):#默认为第一页
    return "您查找的用户为：%s，博客分页为：%s"%(user_id,page)

#查询字符串方式定义参数类型
@app.route('/blog/list')# 定义参数类型
def bolg_list_detail():
    user_id=request.args.get("user_id",default=1,type=int)
    page=request.args.get("page",default=1)
    return f"您查找的用户为：{user_id}，博客分页为：{page}"


@app.route("/blog/add",methods=['POST'])# 定义参数类型
def bolg_add():
    return "使用POST方法添加博客"


@app.route("/blog/add/post/get",methods=['POST','GET'])# 定义参数类型
def bolg_add_post_get():
    if request.method=='GET':
        return "使用GET方法添加博客"
    else:
        return "使用POST方法添加博客"



if __name__ == '__main__':
    app.run()
