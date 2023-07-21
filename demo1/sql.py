from flask import Flask
from flask_sqlalchemy import  SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
HOSTNAME="127.0.0.1"
PORT=3306
USERNAME="root"
PASSWORD="123456"
DATABASE = 'zhiliao'
app.config['SQLALCHEMY_DATABASE_URI']=f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True




#在app.config中设置好连接数据库的信息，然后使用SQLAlchemy(app)创建一个db对象
#SQLAlchemy会自动读取app.config中连接数据库的信息
db=SQLAlchemy(app)
migrate=Migrate(app,db)
# #测试连接
# with app.app_context():
#     with db.engine.connect() as conn:
#         rs=conn.execute("select 1")
#         print(rs.fetchone())#(1,)

#映射
class User(db.Model):
    tablename="user"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)#主键，自增
    username=db.Column(db.String(100),nullable=False)#字符串类型，不为空
    password=db.Column(db.String(100),nullable=False)
#    grade=db.Column(db.String(200))
#添加一条语句，相当于insert
#user=User(username="zhangsan",password='11111')
#
# #同步数据到数据库,不过此方法有局限性
# with app.app_context():
#     db.create_all()
#添加操作
@app.route("/user/add")
def add_user():
    #创建ORM对象
    user = User(username="zhangsan", password='11111')
    #将ORM对象添加到db.session中
    db.session.add(user)
    #将db.session中的改变同步到数据库中
    db.session.commit()
    return "用户创建成功"


#查询操作
@app.route("/user/query")
def query_user():
    #get查找，根据主键查找
    user=User.query.get(1)
    print(f"{user.id}:{user.username}:{user.password}")
    #fitter_by查找,筛选查找
    users=User.query.filter_by(username="zhangsan")
#    users = User.query.filter_by(username="zhangsan")[0]与users=User.query.filter_by(username="zhangsan").first区别
    #都返回第一个数据，但是如果为空，前面那个表示方式会报错，后面那个不报错返回空值
    #还有like，group等查询方式不一一展示
    for user in users:
        print(user.username)
    return "数据查找成功"

#修改操作
@app.route("/user/update")
def update_user():
    user=User.query.filter_by(username="zhangsan")[0]
    user.password="222222"
    db.session.commit()
    return "数据修改成功"

#删除操作
@app.route("/user/delete")
def delete_user():
    #查找
    user=User.query.filter_by(username="zhangsan")[0]
    #从db.session中删除
    db.session.delete(user)
    #将db.session中固定修改，同步到数据库
    db.session.commit()
    return "数据删除成功"


class Article(db.Model):
    tablename = "article"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键，自增
    title = db.Column(db.String(200), nullable=False)  # 字符串类型，不为空
    content=db.Column(db.Text,nullable=False)#文本类型（字数多），不为空
    #添加作者的外键
    authot_id=db.Column(db.Integer,db.ForeignKey("user.id"))
    author=db.relationship("User",backref="articles")
    #backref会自动给模型添加一个articles的属性，用来获取文章列表


#article=Article(title="flask",content="flaskwe12d378yhdcas82u1oiejnsad05645e412231e35sadg1yg1FD2ui3g2132你")
# with app.app_context():
#     db.create_all()

#添加操作
@app.route("/article/add")
def article_user():
    #创建ORM对象
    article1 = Article(title="flask", content="flaskwe12d378yhdcas82u1oiejnsad05645e412231e35sadg1yg1FD2ui3g2132你")
    article1.author=User.query.get(10)

    article2 = Article(title="Django", content="Djangowe12d378yhdcas82u1oiejnsad05645e412231e35sadg1yg1FD2ui3g2132")
    article2.author = User.query.get(10)

    #添加到session中
    db.session.add_all([article1,article2])

    #将db.session中的改变同步到数据库中
    db.session.commit()
    return "文章创建成功"


#查找操作
@app.route("/article/query")
def query_article():
    user=User.query.get(10)
    for article in user.articles:
        print(article.title)
    return "文章查找成功"


#ORM模块映射成表的三步,默认是执行app.py文件
#1.flask db init 执行一次
#2.flask db migrate 识别ORM模型的改变，生成迁移脚本
#3.flask db upgrade 运行迁移脚本，同步到数据库中

@app.route('/')
def hello_world():
    return 'Hello Flask!'



if __name__ == '__main__':
    app.run()
