from flask import Flask,render_template,request,flash
import sqlite3
from flask_cors import CORS
import sqlite3 as sql
from os import path



# TODO make 404 , ... erorrs page
# TODO make concat us and about page 


app = Flask(__name__)
CORS(app)
ROUT = path.dirname(path.relpath((__file__)))
app.secret_key = 'vffn329r0iffasdf939'

def login(): # TODO make a login page for admin 
    pass

def create_post(name,content):
    con = sql.connect(path.join(ROUT,'database.db'))
    cur = con.cursor()
    cur.execute('INSERT INTO post (name,content) VALUES(?, ?)',(name,content))
    con.commit()
    con.close()
    flash('Your post was sent correctly')



def get_post():
    con = sql.connect(path.join(ROUT,'database.db'))
    cur = con.cursor()
    cur.execute('SELECT * FROM post ORDER BY id DESC')
    post = cur.fetchall()
    return post

@app.route('/posts',methods=['GET','POST'])
def show_post():
    show_post = get_post()
    return render_template('posts.html',show_post=show_post)


def likes(): # TODO users can like the posts
    pass

@app.route('/',methods=["GET","POST"])
def index():
    return "this is home page"

@app.route('/send_post',methods=["GET","POST"])
def send_post():  
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        name = request.form.get('name')
        post = request.form.get('post')
        create_post(name,post)
    
    return render_template('send_post.html')

@app.route('/admin_panel') # TODO the admin can log in into admin panel
def admin_panel():
    return "This is admin panel"



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000,debug=True)