#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *

from flask_migrate import Migrate
import sqlalchemy

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
from datetime import datetime
#db.create_all() 

# AK TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/fyyur'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.Integer))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Shows', backref='Venue', lazy=True)

    @property
    def past_shows(self):
        now = datetime.now()
        past_shows = [x for x in self.shows if datetime.strptime(x.start_time, '%Y-%m-%dT%H:%M:%S.%fZ') < now]
        return past_shows    
    @property
    def upcoming_shows(self):
        now = datetime.now()
        upcoming_shows = [x for x in self.shows if datetime.strptime(x.start_time, '%Y-%m-%dT%H:%M:%S.%fZ') > now]
        return upcoming_shows
    @property
    def past_shows_count(self):
        past_shows_count = len(self.past_shows)
        return past_shows_count
    @property
    def upcoming_shows_count(self):
        upcoming_shows_count = len(self.upcoming_shows)
        return upcoming_shows_count
    # AK TODO: implement any missing fields, as a
    #  database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.Integer))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))    
    shows = db.relationship('Shows', backref='Artist', lazy=True)

    @property
    def past_shows(self):
        now = datetime.now()
        past_shows = [x for x in self.shows if datetime.strptime(x.start_time, '%Y-%m-%dT%H:%M:%S.%fZ') < now]
        return past_shows    
    @property
    def past_shows_count(self):
        past_shows_count = len(self.past_shows)
        return past_shows_count
    @property
    def upcoming_shows(self):
        now = datetime.now()
        upcoming_shows = [x for x in self.shows if datetime.strptime(x.start_time, '%Y-%m-%dT%H:%M:%S.%fZ') > now]
        return upcoming_shows
    @property
    def upcoming_shows_count(self):
        upcoming_shows_count = len(self.upcoming_shows)
        return upcoming_shows_count
    # AK TODO: implement any missing fields, as a database migration using Flask-Migrate

class Shows(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    start_time = db.Column(db.String(), nullable=False)
    @property
    def venue_name(self):
        return Venue.query.get(self.venue_id).name
    @property
    def upcoming_shows_count(self):
        return Artist.query.get(self.artist_id).upcoming_shows_count
    @property
    def artist_image_link(self):
        return Artist.query.get(self.artist_id).image_link
    @property
    def venue_image_link(self):
        return Venue.query.get(self.venue_id).image_link
# AK TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  #AK TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  unique_city_states = Venue.query.with_entities( Venue.city, Venue.state).distinct().all() 
  data = [] 
  for city_state in unique_city_states: 
    venues = Venue.query.filter_by(city=city_state[0], state=city_state[1]).all() 
    data.append({'city': city_state[0], 'state': city_state[1], 'venues': venues}) 
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  #AK TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_venue_request = request.form['search_term']
  data_searched=Venue.query.filter(Venue.name.ilike('%{}%'.format(search_venue_request))).all()
  count_venues=len(data_searched)
  response={
    "count": count_venues,
    "data": data_searched
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  #AK TODO: replace with real venue data from the venues table, using venue_id
  data=Venue.query.get(venue_id)
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # AK TODO: insert form data as a new Venue record in the db, instead
  # AK TODO: modify data to be the data object returned from db insertion
  data = request.form
  check_new_venue = Venue.query.filter_by(name=data['name']).all()  
  if len(check_new_venue) > 0:
    flash('An error occurred. Venue ' + request.form['name'] + ' exists!')
    return render_template('pages/home.html')
  try:
    venue = Venue(name=data['name'], city=data['city'], state=data['state'], address=data['address'], phone=data['phone'], genres=[data['genres']], facebook_link=data['facebook_link'])
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('Venue ' + data.name + ' could not be listed.')
  finally:
    db.session.close() 
  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # AK TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  print('here')
  print(venue_id)
  try:
    Venue.query.filter_by(id=venue_id).delete()
  #  db.session.commit()
    flash('Venue deleted')
  except:
    db.session.rollback()
    flash('Not deleted')
  finally:
    db.session.close()
    
  return render_template('pages/home.html')
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # AK TODO: replace with real data returned from querying the database
  data=Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # AK TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_artist_request = request.form['search_term']
  data_searched=Artist.query.filter(Artist.name.ilike('%{}%'.format(search_artist_request))).all()
  count_artists=len(data_searched)
  response={
    "count": count_artists,
    "data": data_searched
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # AK TODO: replace with real venue data from the venues table, using venue_id
  data=Artist.query.get(artist_id)
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist=Artist.query.get(artist_id)
  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.genres.data = artist.genres
  form.facebook_link.data = artist.facebook_link
  # AK TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  data = request.form
  check_new_artist = Artist.query.filter_by(name=data['name']).all()  
  if len(check_new_artist) > 0:
    flash('An error occurred. Artist ' + request.form['name'] + ' exists!')
    return render_template('pages/home.html')
  try:
      artist = Artist(name=data['name'], city=data['city'], state=data['state'], phone=data['phone'], genres=[data['genres']], facebook_link=data['facebook_link'])
      db.session.add(artist)
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
      flash('An error occurred. Artist ' + request.form['name'] + ' not able to list.')
      db.session.rollback()
  finally:
      db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue=Venue.query.get(venue_id)
  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.address.data = venue.address
  form.phone.data = venue.phone
  form.genres.data = venue.genres
  form.facebook_link.data = venue.facebook_link
  # AK TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  data = request.form
  check_new_venue = Venue.query.filter_by(name=data['name']).all()  
  if len(check_new_venue) > 0:
    flash('An error occurred. Venue ' + request.form['name'] + ' exists!')
    return render_template('pages/home.html')
  try:
    venue = Venue(name=data['name'], city=data['city'], state=data['state'], address=data['address'], phone=data['phone'], genres=[data['genres']], facebook_link=data['facebook_link'])
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('Venue ' + data.name + ' could not be listed.')
  finally:
    db.session.close() 
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # AK TODO: insert form data as a new Venue record in the db, instead
  # AK TODO: modify data to be the data object returned from db insertion
  data = request.form
  check_new_artist = Artist.query.filter_by(name=data['name']).all()  
  if len(check_new_artist) > 0:
    flash('An error occurred. Artist ' + request.form['name'] + ' exists!')
    return render_template('pages/home.html')
  try:
      artist = Artist(name=data['name'], city=data['city'], state=data['state'], phone=data['phone'], genres=[data['genres']], facebook_link=data['facebook_link'])
      db.session.add(artist)
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
      flash('An error occurred. Artist ' + request.form['name'] + ' not able to list.')
      db.session.rollback()
  finally:
      db.session.close()
  # on successful db insert, flash success
  # AK TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # AK TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=Shows.query.all()
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  data = request.form
  try:
      show = Shows(artist_id=data['artist_id'], venue_id=data['venue_id'], start_time=data['start_time'])
      db.session.add(show)
      db.session.commit()
      flash('Show was successfully listed!')
  except:
      flash('An error occurred. Show not able to list.')
      db.session.rollback()
  finally:
      db.session.close()
  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
