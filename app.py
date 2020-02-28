from flask import Flask,render_template,request
import sqlite3
from flask_cors import CORS
import sqlite3 as sql
from os import path


# TODO working with flash
# TODO make 404 , ... erorrs page
# TODO make a page for the best psots
# TODO make concat us and about page 


app = Flask(__name__)
CORS(app)
ROUT = path.dirname(path.relpath((__file__)))


def login(): # TODO make a login page for admin 
    pass

def create_post(name,content):
    con = sql.connect(path.join(ROUT,'database.db'))
    cur = con.cursor()
    cur.execute('INSERT INTO post (name,content) VALUES(?, ?)',(name,content))
    con.commit()
    con.close()

def get_post():
    con = sql.connect(path.join(ROUT,'database.db'))
    cur = con.cursor()
    cur.execute('select * from post')
    post = cur.fetchall()
    return post

def likes(): # TODO users can like the posts
    pass


@app.route('/',methods=['GET','POST'])
def index(): # TODO do templates beter 
    
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        name = request.form.get('name')
        post = request.form.get('post')
        create_post(name,post)
    
    show_posts = get_post()
    
    return render_template('index.html',show_posts=show_posts)

@app.route('/admin_panel') # TODO the admin can log in into admin panel
def admin_panel():
    return "This is admin panel"



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)