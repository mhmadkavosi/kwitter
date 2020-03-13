from flask import Flask,render_template,request,flash,redirect, url_for,session, abort,Response
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
import sqlite3 as sql
from os import path
from bs4 import BeautifulSoup 
import urllib.request
import requests
import datetime
import config

app = Flask(__name__)
CORS(app)
ROUT = path.dirname(path.relpath((__file__)))
app.secret_key = config.SECRET_KEY


# flask login 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

USERNAME = config.USERNAME
PASSWORD = config.PASSWORD

# limiter for limiting in login : 5 per 10 minutes
limiter = Limiter(
    app,
    key_func=get_remote_address,
)

class User(UserMixin):

    def __init__(self, id):
        self.id = id
        
    def __repr__(self):
        return "%d" % (self.id)

user = User(0)
 


@login_required
@limiter.limit('5 per 10 minutes')
@app.route("/admin_login", methods=["GET", "POST"])
def login():
    """ this is login page for admin , to admin can login into admin panel """
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




@app.errorhandler(401)
def page_not_found(e):
    return redirect('/admin_login')


     
@login_manager.user_loader
def load_user(userid):
    return User(userid)

@app.route("/logout")
@login_required
@limiter.limit('5 per 10 minutes')
def logout():
    logout_user()
    return redirect('/')



def create_post(name,content,insta_account,time_of_send,insta_url):
    """ we create post into post tabale and save it into database  """
    con = sql.connect(path.join(ROUT,'database.db'))
    cur = con.cursor()
    cur.execute('INSERT INTO post (name,content,insta_account,time_of_send,insta_url) VALUES(?, ?,?,?,?)',(name,content,insta_account,time_of_send,insta_url))
    con.commit()
    con.close()
    flash('Your post was sent correctly')
    



def get_post():
    """ showing the posts , call it from database """
    con = sql.connect(path.join(ROUT,'database.db'))
    cur = con.cursor()
    cur.execute('SELECT * FROM post ORDER BY id DESC')
    post = cur.fetchall()
    return post

def delete_post():
    """ delete posts from database with id  """
    con = sql.connect(path.join(ROUT,'database.db'))
    cur = con.cursor()
    for posts in get_post():
        post_id = posts[0]
        cur.execute('DELETE FROM post WHERE id = {}'.format(post_id))
        delete_post = cur.fetchall()
        con.commit()
        return delete_post



@app.route('/admin_panel',methods=['POST','GET'])
@login_required
@limiter.limit('5 per 10 minutes')
def admin_panel():
    """ this is admin panel in admin panel we showing posts with all content and admin can delete posts """
    show_post = get_post()
    if request.method == 'POST':
        delete_post()
        return render_template('admin_panel.html',show_post=show_post,delete_post=delete_post)
    else:
        return render_template('admin_panel.html',show_post=show_post)


@app.route('/',methods=["GET","POST"])
def index():
    """ this is the index page in this page we just render a template and showing some content """
    return render_template('index.html')

@app.route('/send_post',methods=["GET","POST"])
def send_post():
    """ in here we get information from user with a form and geting the instagram profile and createing the post  """
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
    """ we just showing the post from database"""
    show_post = get_post()
    return render_template('posts.html',show_post=show_post)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000,debug=True)