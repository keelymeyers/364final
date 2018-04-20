# SI 364 - Winter 2018 - Final Project

## App Description 

This application allows users to register/log in to an account and search for movies using the MovieDB API. Once a movie is searched for, data about the top movie result is saved in the Movie model and the top actors for that movie are saved in the Actor model. A user can then see the movies previously searched for, as well as the star actors from searched movies. Additionally, a user can create personal movie collections from searched movies and subsequently delete or rename these collections. 

## Requirements
### Installation Requirements

* flask library and all flask modules used in SI364

### Other

* There must be a file named `moviedb_access.py` in the same directory as `SI364final.py`, with the API key filled in. I have included an API key in the Canvas submission comments for use by the instructors of SI364. For others to run the app, an API key can be generated at https://www.themoviedb.org/documentation/api.


## To Run & Use This Application


* Download and `cd` to the directory where the app files are located.
* In the terminal, run `python SI364final.py runserver`
* At localhost:500, the homepage will display a search form for searching movies, as well as a link at the top to login to the application. All other links are to routes only avaliable to registered/logged in users
* Log in (after registering if necessary)
* Once logged in, there will be a form to search movie titles. Enter a movie title to search the API.
    * For example, search "Black Panther" in the search box.
    * You should see a message alerting you that the movie has been added to searched movies, or a message saying that the movie could not be found
    * If the API request returns a result, the movie title & release date will be saved to the Movie model, and the names of the top actors will be saved in the Actor model, with a many:many relationship between the two.
* Once a movie has been searched for, you can click "See all movies" to see a list of all searched movies, or "See all actors" to see all the actors who star in movies you have searched for. Each view function will query their respective database.
* You can then click "Create a personal movie collection", where you will be prompted to choose a name for a movie collection, such as "Movies to Watch", and then select movies to add. The collection will then be saved to the PersonalMovieCollection model.
* After creating a collection, you can click "See all collections", where a list will appear of all of your user-specific collections, alongside Update and Delete buttons. You can either click on the collection name to see movies in the collection, or click either the Delete or Update button. The Delete button will delete your collection, and the Update button will allow you to change the name of your collection. Each feature will either update or delete data in the PersonalMovieCollection model.


## Routes in this Application

* `/login` -> `login.html`
* `/logout` -> Logs out current user and redirects to the homepage ('/') (login restricted)
* `/register` -> `register.html` 
* `/` -> `base.html`
* `/actors` -> `all_actors.html` (login restricted)
* `/movies` -> `all_movies.html` (login restricted)
* `/create_movie_collection` -> `create_collection.html` (login restricted)
* `/collections` -> `collections.html` (login restricted)
* `/collection/<id_num>` -> `collection.html` (login restricted)
* `/delete/<collection>` -> Deletes a collection and redirects to collections page (login restricted)
* `/update/<collection>` -> `update_collection.html` (login restricted)


## Code Requirements
Note that many of these requirements of things your application must DO or must INCLUDE go together! Note also that you should read all of the requirements before making your application plan***.***

 - [x] **Ensure that your SI364final.py file has all the setup (app.config values, import statements, code to run the app if that file is run, etc) necessary to run the Flask application, and the application runs correctly on http://localhost:5000 (and the other routes you set up). Your main file must be called SI364final.py, but of course you may include other files if you need.**

 - [x] **A user should be able to load http://localhost:5000 and see the first page they ought to see on the application.**

 - [x] **Include navigation in base.html with links (using a href tags) that lead to every other page in the application that a user should be able to click on. (e.g. in the lecture examples from the Feb 9 lecture, like this )**

 - [x] **Ensure that all templates in the application inherit (using template inheritance, with extends) from base.html and include at least one additional block.**

 - [x] **Must use user authentication (which should be based on the code you were provided to do this e.g. in HW4).**

 - [x] **Must have data associated with a user and at least 2 routes besides logout that can only be seen by logged-in users.**

 - [x] **At least 3 model classes besides the User class.**

- [ ] At least one one:many relationship that works properly built between 2 models.

 - [x] **At least one many:many relationship that works properly built between 2 models.**

 - [x] **Successfully save data to each table.**

 - [x] **Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for) and use it to effect in the application (e.g. won't count if you make a query that has no effect on what you see, what is saved, or anything that happens in the app).**

 - [x] **At least one query of data using an .all() method and send the results of that query to a template.**

 - [x] **At least one query of data using a .filter_by(... and show the results of that query directly (e.g. by sending the results to a template) or indirectly (e.g. using the results of the query to make a request to an API or save other data to a table).**

 - [x] **At least one helper function that is not a get_or_create function should be defined and invoked in the application.**

 - [x] **At least two get_or_create functions should be defined and invoked in the application (such that information can be saved without being duplicated / encountering errors).**

 - [x] **At least one error handler for a 404 error and a corresponding template.**

 - [x] **At least one error handler for any other error (pick one -- 500? 403?) and a corresponding template.**

 - [x] **Include at least 4 template .html files in addition to the error handling template files.**

 - [x] **At least one Jinja template for loop and at least two Jinja template conditionals should occur amongst the templates.**
 
 - [x]**At least one request to a REST API that is based on data submitted in a WTForm OR data accessed in another way online (e.g. scraping with BeautifulSoup that does accord with other involved sites' Terms of Service, etc).**

 - [x] **Your application should use data from a REST API or other source such that the application processes the data in some way and saves some information that came from the source to the database (in some way).**
 
- [ ] At least one WTForm that sends data with a GET request to a new page.

 - [x] **At least one WTForm that sends data with a POST request to the same page. (NOT counting the login or registration forms provided for you in class.)**

 - [x] **At least one WTForm that sends data with a POST request to a new page. (NOT counting the login or registration forms provided for you in class.)**

 - [x] **At least two custom validators for a field in a WTForm, NOT counting the custom validators included in the log in/auth code.**

 - [x] **Include at least one way to update items saved in the database in the application (like in HW5).**

 - [x] **Include at least one way to delete items saved in the database in the application (also like in HW5).**

 - [x] **Include at least one use of redirect.**

 - [x] **Include at least two uses of url_for. (HINT: Likely you'll need to use this several times, really.)**

 - [x] **Have at least 5 view functions that are not included with the code we have provided. (But you may have more! Make sure you include ALL view functions in the app in the documentation and navigation as instructed above.)**

Additional Requirements for additional points -- an app with extra functionality!
Note: Maximum possible % is 102%.

- [ ](100 points) Include a use of an AJAX request in your application that accesses and displays useful (for use of your application) data.
- [ ](100 points) Create, run, and commit at least one migration.
- [ ](100 points) Include file upload in your application and save/use the results of the file. (We did not explicitly learn this in class, but there is information available about it both online and in the Grinberg book.)
- [ ](100 points) Deploy the application to the internet (Heroku) — only counts if it is up when we grade / you can show proof it is up at a URL and tell us what the URL is in the README. (Heroku deployment as we taught you is 100% free so this will not cost anything.)
- [ ](100 points) Implement user sign-in with OAuth (from any other service), and include that you need a specific-service account in the README, in the same section as the list of modules that must be installed.
