from flask import Flask, render_template, send_from_directory
from os.path import join
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager

app = Flask(__name__)
DEBUG = False


descriptions = {
    'flask': '''
        This demo is a simple author/news article manager. Authors may have many
        articles and are related by an <code>person_id</code>. The demo shows
        two views for People. Basic shows the out of the box view on a model,
        very little configuration necessary, while Advanced explores some of the
        more useful functionalities of Can-Admin.
        '''
}

@app.route('/')
@app.route('/<string:page>')
@app.route('/<string:page>/<path:config_path>')
def page(page='home', config_path='flask'):
    return render_template(
        'pages/{}.html.j2'.format(page),
        config_path='can-crud-app/config/{0}/{0}'.format(config_path), debug=DEBUG,
        description=descriptions[config_path]
    )

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
