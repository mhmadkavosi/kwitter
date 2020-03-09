from flask import Flask,render_template,request,flash,redirect, url_for,session, abort,Response
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
import sqlite3
from flask_cors import CORS
import sqlite3 as sql
from os import path
from bs4 import BeautifulSoup 
import urllib.request
import requests
import datetime

# TODO make delete post for delete post form admin panel

app = Flask(__name__)
CORS(app)
ROUT = path.dirname(path.relpath((__file__)))
app.secret_key = 'vffn329r0iffasdf939'

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

USERNAME = "mohammad"
PASSWORD = "kavosi"

# silly user model
class User(UserMixin):

    def __init__(self, id):
        self.id = id
        
    def __repr__(self):
        return "%d" % (self.id)

user = User(0)
 
# somewhere to login
@app.route("/admin_login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']        
        if password == PASSWORD and username == USERNAME:
            login_user(user)
            return redirect("/admin_panel")
        else:
            return abort(401)
    else:
        return render_template('login.html')



# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return redirect('/admin_login')


# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    return User(userid)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('you logou as well')
    return redirect('/admin_login')



def create_post(name,content,insta_account,time_of_send,insta_url):
    con = sql.connect(path.join(ROUT,'database.db'))
    cur = con.cursor()
    cur.execute('INSERT INTO post (name,content,insta_account,time_of_send,insta_url) VALUES(?, ?,?,?,?)',(name,content,insta_account,time_of_send,insta_url))
    con.commit()
    con.close()
    flash('Your post was sent correctly')
    



def get_post():
    con = sql.connect(path.join(ROUT,'database.db'))
    cur = con.cursor()
    cur.execute('SELECT * FROM post ORDER BY id DESC')
    post = cur.fetchall()
    return post




@app.route('/admin_panel',methods=['POST','GET'])
@login_required
def admin_panel():
    show_post = get_post()
    return render_template('admin_panel.html',show_post=show_post)

def likes(): # TODO users can like the posts
    pass

@app.route('/',methods=["GET","POST"])
def index():
    return render_template('index.html')

@app.route('/send_post',methods=["GET","POST"])
def send_post():
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        name = request.form.get('name')
        post = request.form.get('post')
        insta_account = request.form.get('insta_account')
        time_of_send = datetime.datetime.now()
        html=urllib.request.urlopen("https://instagram.com/"+insta_account)
        soup=BeautifulSoup(html,features="html.parser")
        insta_url = soup.find("meta",{"property":"og:image"})['content']
        create_post(name,post,insta_account,time_of_send,insta_url)
    
    return render_template('send_post.html')

@app.route('/posts',methods=['GET','POST'])
def show_post():
    show_post = get_post()
    return render_template('posts.html',show_post=show_post)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000,debug=True)