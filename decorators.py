from functools import  wraps
from flask import g,redirect,url_for



# 装饰器
def login_required(func):
    #保留func的信息
    @wraps(func)
    #func(a,b,c=3),a,b在*args中，c=3在**kwargs
    def inner(*args,**kwargs):
        if g.user:#判断g是否有值
            return func(*args,**kwargs)
        else:
            return redirect(url_for("auth.login"))
    return inner

