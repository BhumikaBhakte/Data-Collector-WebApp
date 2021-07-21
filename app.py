from flask import Flask, render_template,request
#from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func

app=Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres123@localhost/height_collector'
app.config['SQLALCHEMY_DATABASE_URI']='postgres://hpfhytmzjdknsg:4e16329355642bb2bbad4b6f808449da4d1a532a4126bf7a6acf42fc0e16cee3@ec2-34-194-14-176.compute-1.amazonaws.com:5432/dfaomvsuuithsb?sslmode=require'.replace('postgres://', 'postgresql://')
db=SQLAlchemy(app)

class Data(db.Model):
    __tablename__="data"
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(120), unique=True)
    height_=db.Column(db.Integer)

    def __init__(self,email_,height_):
        self.email_=email_
        self.height_=height_


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/success',methods=['POST'])
def success():
    if request.method=='POST':
        email=request.form["email_name"]
        height=request.form["height_name"]

        if db.session.query(Data).filter(Data.email_==email).count()==0:
            data=Data(email,height)
            db.session.add(data)
            db.session.commit()
            avg_height=db.session.query(func.avg(Data.height_)).scalar()
            avg_height=round(avg_height,1)
            count=db.session.query(Data.height_).count()
            send_email(email,height,avg_height,count)
            return render_template("success.html")
    return render_template("index.html", text="Seems like we've got something from that email already!")

if __name__=='__main__':
    app.debug=False
    app.run()
