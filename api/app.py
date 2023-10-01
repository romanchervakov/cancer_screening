import datetime
import pytz
import random
from flask import render_template, request, redirect, url_for
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba111'
app.config['SQLALCHEMY_DATABASE_URI'] = ('postgresql://uqmsiv4msken1z8u9jbr:'
                                         'ScqDwM7eRnwZOy8DtwESB06fmkiPCD@'
                                         'bgvj1gcg7xvieqm7pey1-postgresql.services.clever-cloud.com:5432/'
                                         'bgvj1gcg7xvieqm7pey1')
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300
}
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class CancerAwarenessQuestionnaireOutside(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inner_table_id = db.Column(db.Integer)
    number = db.Column(db.Integer)
    suspicion = db.Column(db.Boolean)
    question1 = db.Column(db.Boolean)
    question2 = db.Column(db.Boolean)
    question3 = db.Column(db.Boolean)
    question4 = db.Column(db.Boolean)
    question5 = db.Column(db.Boolean)
    question6 = db.Column(db.Boolean)
    question7 = db.Column(db.Boolean)
    question8 = db.Column(db.Boolean)
    question9 = db.Column(db.Boolean)
    date_sent = db.Column(db.DateTime)


suspicion = False


@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        global suspicion

        def convert(answer):
            global suspicion
            if answer == 'yes':
                suspicion = True
                return True
            else:
                return False

        numbers_raw = CancerAwarenessQuestionnaireOutside.query.with_entities(
            CancerAwarenessQuestionnaireOutside.number).all()
        numbers = []
        for number in numbers_raw:
            numbers.append(number.number)
        number = random.randint(100000, 300000)
        while number in numbers:
            number = random.randint(100000, 300000)

        q = CancerAwarenessQuestionnaireOutside()
        q.number = number
        q.question1 = convert(request.form['rq1'])
        q.question2 = convert(request.form['rq2'])
        q.question3 = convert(request.form['rq3'])
        q.question4 = convert(request.form['rq4'])
        q.question5 = convert(request.form['rq5'])
        q.question6 = convert(request.form['rq6'])
        q.question7 = convert(request.form['rq7'])
        q.question8 = convert(request.form['rq8'])
        q.question9 = convert(request.form['rq9'])
        q.suspicion = suspicion
        q.date_sent = datetime.datetime.now(pytz.timezone("Europe/Moscow")).strftime("%Y-%m-%d %H:%M:%S")
        db.session.add(q)
        db.session.commit()

        return redirect(url_for('result', number=number, status=suspicion))

    return render_template("form.html")


@app.route('/result/<int:number>/<int:status>')
def result(number, status):
    return render_template("result.html", status=status, number=number)


