from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required, LoginManager, UserMixin
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
#import NoFluffJobs


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SECRET_KEY'] = 'asdasdasd'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
# login_manager.login_message_category =

#Modele

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable = False)
    password = db.Column(db.String(50), nullable = False)
    join_date = db.Column(db.DateTime, default = datetime.utcnow)
    search_id = db.relationship('Search', backref = 'ovner', lazy = True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.id



class Search(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    keyword = db.Column(db.String(50), nullable = False)
    location = db.Column(db.String(50), nullable = False)
    offers_id = db.relationship('Offer', backref = 'wyszukiwanie', lazy = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return '<Search %r>' % self.id

class Offer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable = False)
    company = db.Column(db.String(50), nullable = False)
    salary = db.Column(db.Numeric(precision=2, asdecimal=False, decimal_return_scale = None))
    reflink = db.Column(db.String(50), nullable = False)
    search_id = db.Column(db.Integer, db.ForeignKey('search.id'), nullable = False)


    def __init__(self, keyword, localisation):
         self.keyword = keyword
         self.localisation = localisation

    def __repr__(self):
            return '<Oferta %r>' % self.id


#Formy

class RegForm(FlaskForm):
    username = StringField('username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Nazwa użytkownika zajęta wybierz inną')

class LogForm(FlaskForm):
    username = StringField('username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SearchForm(FlaskForm):
    keyword = StringField('keyword',
                        validators=[DataRequired(), Length(min=2, max=20)])
    location = StringField('location',
                        validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Znajdz')


#Routy

@app.route('/', methods = ['POST','GET'])
def index():
    return render_template('index.html')

@app.route('/search',methods = ['POST','GET'])
def search():

    form = SearchForm()
    if current_user.is_authenticated:
        return render_template('search.html', form = form )


    if form.validate_on_submit():
        search1 = Search(keyword=form.keyword, location=form.location, user_id=current_user)
        db.session.add(search1)
        db.session.commit()
        return render_template('offers.html', form = form, search1 = search1)


    return render_template('login.html', form = form )

@app.route('/offers',methods=['POST','GET'])
def offers(search1):
    jobList = NoFluffJobs.Scrape(search1.keyword,search1.location,1,6)
    return render_template('offers.')

@app.route('/register',methods = ['POST','GET'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegForm()

    if form.validate_on_submit():
            hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, password=hashedPassword)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))

    return render_template('register.html', form = form )

@app.route('/login',methods = ['POST','GET'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LogForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            return redirect(url_for('index'))
        else:
            return "Błąd logowania!!!"

    return render_template('login.html', form = form)

@login_required
@app.route('/logout')
def logout():

    logout_user()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)

