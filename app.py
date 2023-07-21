from flask import Flask,session,g
import config
from exts import db,mail
from flask_sqlalchemy import  SQLAlchemy
from flask_migrate import Migrate
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp



app = Flask(__name__)
#绑定配置文件
app.config.from_object(config)

db.init_app(app)#将db对象与app对象，这里先创建db对象，再将db对象绑定，不是一创建就绑定，主要用于解决代码分离问题，防止代码循环
mail.init_app(app)

migrate=Migrate(app,db)

app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)
#blueprint 蓝图,放置视图函数


#before_request/ before_first_request/ after_request
#hook钩子函数
@app.before_request
def my_before_requset():
    user_id = session.get("user_id")
    if user_id:
        user=UserModel.query.get(user_id)
        setattr(g,"user",user)
    else:
        setattr(g,"user",None)

#上下文处理器
@app.context_processor
def my_context_processor():
    return {"user":g.user}




if __name__ == '__main__':
    app.run()
