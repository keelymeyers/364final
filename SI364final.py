# Import statements

import os
import requests
import json
from moviedb_access import api_key
from flask import Flask, render_template, session, redirect, request, url_for, flash
from flask_script import Manager, Shell
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, PasswordField, BooleanField, SelectMultipleField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from werkzeug.security import generate_password_hash, check_password_hash

# Imports for login management
from flask_login import LoginManager, login_required, logout_user, login_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Application configurations
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hardtoguessstring'
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL') or "postgresql://localhost/SI364finalKEELYM" 
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['HEROKU_ON'] = os.environ.get('HEROKU')


# App addition setups
manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

# Login configurations setup
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app) 


########################
######## Models ########
########################


## Association tables

movie_cast = db.Table('movie_cast',db.Column('movie_id',db.Integer, db.ForeignKey('movies.id')),db.Column('actor_id',db.Integer, db.ForeignKey('actors.id')))
user_collection = db.Table('user_collection',db.Column('user_id', db.Integer, db.ForeignKey('movies.id')),db.Column('collection_id',db.Integer, db.ForeignKey('personalMovieCollections.id')))


## User-related Models

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

## DB load function

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 


class Movie(db.Model):
	__tablename__ = "movies"
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(256))
	release_date = db.Column(db.String(25))
	cast = db.relationship('Actor',secondary=movie_cast,backref=db.backref('movies',lazy='dynamic'),lazy='dynamic')

class Actor(db.Model):
	__tablename__ = "actors"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(256))
	#cast = db.relationship('Movie',backref=)

class PersonalMovieCollection(db.Model):
	__tablename__ = "personalMovieCollections"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(256))
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
	movies = db.relationship('Movie',secondary=user_collection,backref=db.backref('personalMovieCollections',lazy='dynamic'),lazy='dynamic')



########################
######## Forms #########
########################


class RegistrationForm(FlaskForm):
    email = StringField('Email:', validators=[Required(),Length(1,64),Email()])
    username = StringField('Username:',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField('Password:',validators=[Required(),EqualTo('password2',message="Passwords must match")])
    password2 = PasswordField("Confirm Password:",validators=[Required()])
    submit = SubmitField('Register User')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

# Movie title search form

class MovieSearchForm(FlaskForm):
    title = StringField("Enter a valid movie title to search movies", validators=[Required()])
    submit = SubmitField('Submit')

    def validate_title(self,field):

    	if field.data[0] != field.data[0].upper():
        	raise ValidationError('Please capitalize the name of the movie!')


# Movie actors search form 

# Movie Collection Create Form

class CreateMovieCollectionForm(FlaskForm):
    name = StringField('Movie Collection Name',validators=[Required()])
    movie_picks = SelectMultipleField('Movies to include')
    submit = SubmitField("Create Collection")

    def validate_name(self, field):
    	min_char = 3
    	max_char = 70
    	if len(field.date) < min_char:
    		raise ValidationError('Name must be 3-70 characters!')
    	if len(field.data) > 70:
    		raise ValidationError('Name must be 3-70 characters!')

   

class UpdateButtonForm(FlaskForm):
    submit = SubmitField('Update')


class UpdateCollectionName(FlaskForm):
    newName = StringField("What is the new name of this collection?", validators=[Required()])
    submit = SubmitField('Update')

    def validate_newName(self,field):
    	if len(field.data) < 3:
    		raise ValidationError('Name must be 3-70 characters!')
    	if len(field.data) > 70:
    		raise ValidationError('Name must be 3-70 characters!')


class DeleteButtonForm(FlaskForm):
    submit = SubmitField('Delete')



########################
### Helper functions ###
########################


def get_movie_by_id(id):
    m = Movie.query.filter_by(id=id).first()
    return m


def get_or_create_actor(db_session, name, movies=[]):
	actor = db_session.query(Actor).filter_by(name=name).first()
	if actor:
		return actor
	else: 
		actor = Actor(name=name)
		db_session.add(actor)
		db_session.commit()
		return actor

def get_or_create_movie(db_session, title, release_date, cast):
	movie = db_session.query(Movie).filter_by(title=title, release_date=release_date).first()
	if movie:
		return movie
	else: 
		movie = Movie(title=title, release_date=release_date)
		for a in cast:
			actor = get_or_create_actor(db_session, a)
			movie.cast.append(actor)
		db_session.add(movie)
		db_session.commit()
		return movie


def get_or_create_movie_collection(db_session, name, current_user, movie_list):
    movieCollection = db_session.query(PersonalMovieCollection).filter_by(name=name,user_id=current_user.id).first()
    if movieCollection:
        return movieCollection
    else:
        movieCollection = PersonalMovieCollection(name=name,user_id=current_user.id,movies=[])
        for m in movie_list:
            movieCollection.movies.append(m)
        db_session.add(movieCollection)
        db_session.commit()
        return movieCollection

def searchMovieTitle(titleSearch):
	movie = titleSearch
	m = requests.get("https://api.themoviedb.org/3/search/movie?api_key=" + api_key + "&query="+movie)
	movie_data = json.loads(m.text)
	print(movie_data)
	movie_id = movie_data["results"][0]["id"]
	movie_title = movie_data["results"][0]["original_title"]
	release_date = movie_data["results"][0]["release_date"]
	c = requests.get("https://api.themoviedb.org/3/movie/"+str(movie_id)+"/credits?api_key=9b0e6cc4926c841a3e1ddeaa17e76b10&language=en-US")
	movie_credits = json.loads(c.text)
	cast = []
	for actor in movie_credits["cast"][:5]:
		cast.append(actor["name"])
	movie_results = (movie_title, release_date, str(cast[:5]))
	get_or_create_movie(db.session, title=movie_title, release_date=release_date, cast=cast)
	return movie_results


########################
#### View functions ####
########################


@app.errorhandler(404)   # 404 Error Handler
def page_not_found(e):
    return render_template('404.html'), 404



@app.errorhandler(500)    # 500 Error Handler
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/login',methods=["GET","POST"])     # Login route, renders login form and allows user to sign into account
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password.')
    return render_template('login.html',form=form)


@app.route('/logout')   # Logout route
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))


@app.route('/register',methods=["GET","POST"])   #Register user route, allows user to make a new account and then login
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now log in!')
        return redirect(url_for('login'))
    return render_template('register.html',form=form)


@app.route('/', methods=['GET', 'POST'])   
def index():
	form = MovieSearchForm()
	if request.method=='POST':
		if form.validate_on_submit():
			searchMovieTitle(str(form.title.data))
			name = searchMovieTitle(str(form.title.data))[0]
			return render_template('base.html', form=form, name=name)
		flash("Sorry! Movie not found. Try checking your spelling and try again")
		return render_template('base.html',form=form)
	return render_template('base.html',form=form)


@app.route('/actors')
@login_required
def see_all_actors():
	all_actors = Actor.query.all()
	return render_template('all_actors.html', all_actors=all_actors)
	

@app.route('/movies')
@login_required
def see_all():
	all_movies = Movie.query.all()
	return render_template('all_movies.html',all_movies=all_movies)


@app.route('/create_movie_collection', methods=["GET","POST"])
@login_required
def create_collection():
    form = CreateMovieCollectionForm()
    movies = Movie.query.all()
    choices = [(m.id, m.title) for m in movies]
    form.movie_picks.choices = choices
    if request.method=='POST':
        movie_picks = form.movie_picks.data
        movie_objects = [get_movie_by_id(int(id)) for id in movie_picks]
        get_or_create_movie_collection(db.session,current_user=current_user,movie_list=movie_objects,name=form.name.data)
        return redirect(url_for('collections'))
    return render_template('create_collection.html',form=form)

 	# This route will render a template allowing users to create collections of movies based on movies they have searched so far. It will allow them to enter a name for the collection and select multiple options from a list of searched movies.

@app.route('/collections',methods=["GET","POST"])
@login_required
def collections():
	form1 = DeleteButtonForm()
	form2 = UpdateButtonForm()
	collections = PersonalMovieCollection.query.filter_by(user_id=current_user.id).all()
	return render_template('collections.html', collections=collections, delete=form1, update=form2)

    # This route will query the personalMovieCollections database and render a template with all of the current user's personal movie collections. It will display a list of all the links to these collections as well as buttons to delete or update collections.

@app.route('/collection/<id_num>')
def single_collection(id_num):
	id_num = int(id_num)
	collection = PersonalMovieCollection.query.filter_by(id=id_num).first()
	movies = collection.movies.all()
	return render_template('collection.html',collection=collection, movies=movies)

	# This route will display the movies for one specific collection. 

@app.route('/delete/<collection>',methods=["GET","POST"])
def delete(collection):
    c = PersonalMovieCollection.query.filter_by(name=collection).first()
    db.session.delete(c)
    db.session.commit()
    flash("Deleted collection "+collection)
    return redirect(url_for('collections'))

	# This code should render a form that allows users to delete the appropriate collection and flash the name of the collection that was deleted.



@app.route('/update/<collection>', methods=["GET", "POST"])
def update(collection):
    form = UpdateCollectionName()
    if form.validate_on_submit():
        print(collection)
        new_name = form.newName.data
        c = PersonalMovieCollection.query.filter_by(name=collection).first()
        c.name = new_name
        db.session.commit()
        flash("Changed name of " + collection + " to " + c.name)
        return redirect(url_for('collections'))
    return render_template('update_collection.html',collection = collection, form = form)



	# This code should render a form that allows users to update the name of the appropriate collection and redirect to the view function showing links for all collections. It should also flash a messaged saying "updated <collection_name>"



if __name__ == "__main__":
    db.create_all()
    manager.run()




