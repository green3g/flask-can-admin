from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager

app = Flask(__name__)


@app.route('/')
@app.route('/<path:config_path>')
def hello_world(config_path='can-crud-app/config/flask/'):
    return render_template('admin.html', config_path=config_path)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
manager = APIManager(app, flask_sqlalchemy_db=db)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone_number = db.Column(db.String(11))
    address = db.Column(db.String(500))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    zip_code = db.Column(db.Integer())
    is_cool = db.Column(db.Boolean)
    birthday = db.Column(db.Date)
    picture = db.Column(db.String(500))

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    author = db.relationship(Person, backref=db.backref('articles'))
    title = db.Column(db.String(100))
    content = db.Column(db.Text())
    reviewed = db.Column(db.Integer)

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)

db.create_all()

methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH' ]
manager.create_api(Person, methods=methods)
manager.create_api(Article, methods=methods)
manager.create_api(Visit, methods=methods)

if __name__ == '__main__':
    app.run(debug=True)
