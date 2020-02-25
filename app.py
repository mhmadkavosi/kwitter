from flask import Flask,render_template,request
import sqlite3
from flask_cors import CORS
import sqlite3 as sql
from os import path

app = Flask(__name__)

CORS(app)
ROUT = path.dirname(path.relpath((__file__)))


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


@app.route('/',methods=['GET','POST'])
def index():
    
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        name = request.form.get('name')
        post = request.form.get('post')
        create_post(name,post)
    
    show_posts = get_post()
    
    return render_template('index.html',show_posts=show_posts)





if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)