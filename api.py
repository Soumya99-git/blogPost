from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///posts.db"
db = SQLAlchemy(app)

class BlogPosts(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(20),nullable=False)
    content = db.Column(db.Text,nullable=False)
    author = db.Column(db.String(20),nullable=False,default="No Author Given")


    def __repr__(self):
        return "Blog"+" "+str(self.id)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/create",methods=["GET","POST"])
def createpost():
    if request.method=="POST":
        p_title = request.form["title"]
        p_content = request.form["content"]
        p_author = request.form["author"]
        new = BlogPosts(title=p_title,content=p_content,author=p_author)
        db.session.add(new)
        db.session.commit()
        return redirect("/posts")
    else: 
        return render_template("create.html")


@app.route("/posts",methods=["GET","POST"])
def post():
    if request.method =="POST":
        p_title = request.form["title"]
        p_content = request.form["content"]
        p_author = request.form["author"]
        new = BlogPosts(title=p_title,content=p_content,author=p_author)
        db.session.add(new)
        db.session.commit()
        return redirect("/posts")
    else:
        new_post = BlogPosts.query.all()
        return render_template("posts.html",post = new_post)

@app.route("/posts/delete/<int:id>")
def delete(id):
    i = BlogPosts.query.get_or_404(id)
    db.session.delete(i)
    db.session.commit()
    return redirect("/posts")

@app.route("/posts/edit/<int:id>",methods = ["GET","POST"])
def edit(id):
    i = BlogPosts.query.get_or_404(id)

    if request.method=="POST":
        i.title = request.form['title']
        i.content =request.form['content']
        i.author = request.form['author']
        db.session.add(i)
        db.session.commit()
        return redirect("/posts")
    else:
        return render_template("edit.html",posts=i)
if __name__ == "__main__":
    app.run(debug=True)