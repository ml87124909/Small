# -*- coding: utf-8 -*-
#start.py


import os, sys, traceback, time,requests
from imp import reload
reload(sys)

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)
sys.stdout = sys.stderr

from flask import Flask, request,redirect,render_template
from flask_cors import CORS
from sqlalchemy import *


app=Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RTYj'
CORS(app)
#不判断副文本

filename = "{}/dbconfig.py".format(app.root_path)



def create_config(username, password, host,port, dbname):
    data = render_template("config.html",username=username,password=password,host=host,port=port,dbname=dbname)
    fd = open(filename, "w")
    fd.write(data)
    fd.close()

@app.route('/install', methods=['GET', 'POST'])
def install():
    code=0
    if os.path.exists(filename):
        code=3
    return render_template('install.html',code=code)

@app.route('/setup', methods=['GET', 'POST'])
def setup():

    step = request.args.get("step", type=int)
    RES = request.values
    if step == 1:
        return render_template("setup1.html")
    elif step == 2:

        host = RES.get('host','')
        username = RES.get('username','')
        passwd = RES.get('passwd','')
        dbname = RES.get('dbname','')
        port = RES.get('port','')

        url = 'postgresql+psycopg2://%s:%s@%s:%s/%s' % (username, passwd, host,port,dbname)
        try:
            engine_ = create_engine(url)
            connection = engine_.connect()
        except:
            return render_template("setup-error.html", code=3)

        create_config(username, passwd, host, port,dbname)
        if os.path.exists(filename):
            from models.model import createall
            createall(engine_)
            return render_template("setup2.html")
        return render_template("setup-error.html", code=3)


    elif step == 3:
        login_id = RES.get('login_id', '')
        passwd = RES.get('passwd', '')
        try:
            from models.model import DBSession,User
            session = DBSession()
            user = session.query(User).filter_by(username=login_id).first()
            if user is not None:

                session.query(User).filter(User.username == login_id).update({"password":passwd})
                session.commit()
                session.close()
                return render_template('setup.html',code=0)
            user = User()
            user.username = login_id
            user.nickname = login_id
            user.password =passwd

            session.add(user)
            session.commit()
            session.close()

            return render_template('setup.html',code=0)
        except:
            return render_template('setup.html', code=3)
    return render_template('install.html')



@app.route('/', methods=['GET', 'POST'])
def start():
    if not os.path.exists(filename):
        return redirect('/install')
    return render_template('ok.html')



if __name__ == '__main__':
    #app.run(port=5001)
    app.run(host='127.0.0.1', port=5001,debug=True)




