# flask-sqlalchemy
#此文件主要用来解决循环引用问题
#部分配置文件放在此处，代码分离，防止循环引用
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


db=SQLAlchemy()#给models.py和app.py引用
mail = Mail()#邮箱对象