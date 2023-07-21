from flask import Blueprint,request,render_template,g,redirect,url_for
from .forms import QuestionForm,AnswerForm
from models import QuestionModel,AnswerModel
from exts import db
from decorators import login_required

bp=Blueprint("qa",__name__,url_prefix="/")#根路径

@bp.route("/")
def index():
    questions=QuestionModel.query.order_by(QuestionModel.creat_time.desc()).all()
    return render_template("index.html",questions=questions)

@bp.route("/qa/public",methods=['GET','POST'])
@login_required
def public_question():
    # if not g.user:
    #     return redirect(url_for("qa.public_question"))
    if request.method=='GET':
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():#如果验证成功
            title=form.title.data
            content=form.content.data
            question=QuestionModel(title=title,content=content,author=g.user)
            db.session.add(question)
            db.session.commit()
            #跳转到详情页
            return redirect("/")
        else:
            print(form.errors)
            return redirect(url_for("qa.public_question"))


@bp.route("/qa/detail/<qa_id>")
def qa_detail(qa_id):
    question=QuestionModel.query.get(qa_id)
    return render_template("detail.html",question=question)

@bp.route("/answer/pubilc",methods=['POST'])
#@bp.post("/answer/pubilc") 也可以，代表用POST请求
@login_required
def public_answer():
    form=AnswerForm(request.form)
    if form.validate():
        content=form.content.data
        question_id=form.question_id.data
        answer=AnswerModel(content=content,question_id=question_id,author_id=g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("qa.qa_detail",qa_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for("qa.qa_detail",qa_id=request.form.get("question_id")))


@bp.route("/search")
def search():
    # /search？q=flask
    # /search/<q>
    # post,request.form
    q=request.args.get("q")#获取参数 q
    questions=QuestionModel.query.filter(QuestionModel.title.contains(q)).all()#过滤查找,把名字中包含关键字q的都搜索出来
    return render_template("index.html",questions=questions)
