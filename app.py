from flask import (Flask,
                   render_template,
                   flash, redirect,
                   url_for,
                   session,
                   logging
                   )
from flask.globals import request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

from data import Articles

Articles = Articles()

app = Flask(__name__)


# config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'Fachiis'
app.config['MYSQL_PASSWORD'] = 'zasha1996'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init MYSQL
mysql = MySQL(app)


@app.route('/')  # defining the route for the homepage
def index():
    return render_template('home.html')


@app.route('/about')  # defining the route for the aboutpage
def about():
    return render_template('about.html')


@app.route('/articles')  # defining the route for the articlespage
def articles():
    return render_template('articles.html', articles=Articles)


@app.route('/article/<string:id>/')  # defining the route for each article page
def article(id):
    return render_template('article.html', id=id)


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute(
            "INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (
                name, email, username, password)
        )

        # Commit to DB
        mysql.connection.commit()

        # Close  connection
        cur.close()

        # Message after success registration
        flash('You are now registered and can log in', 'success')

        return redirect(url_for('index'))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.secret_key = '#31761996zasha'
    app.run(debug=True)  # This code actually allows us to start the application
