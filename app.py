#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import (
  Flask, 
  render_template, 
  request, 
  flash, 
  redirect, 
  url_for
)

from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import db, Venue, Artist, Show
from flask_migrate import Migrate

#================================================================#
#=====================Controller Imports=========================#
#================================================================#
from controllers import venue, artist


#=================================================================#
#                       App Config.
#=================================================================#

def create_app():
  app = Flask(__name__)
  app.config.from_object('config')

  with app.app_context():
    db.init_app(app)
  return app

app = create_app()
moment = Moment(app)

# TODO: connect to a local postgresql database
migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#===========================================================================#
#                             Controllers.
#===========================================================================#

@app.route('/')
def index():
  return render_template('pages/home.html')


#=================================================================#
#========================= Venues ================================#
#  ---------------------------------------------------------------#

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

  data = venue.venue()

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])


#==================================================================#
#========================== SEARCH VENUES =========================#

def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  search_term=request.form.get('search_term', '')
  response = venue.search_venue(search_term)

  return render_template('pages/search_venues.html', results=response)



#======================================================================#
#========================= SHOW VENUE =================================#
#======================================================================#

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_i

  venue_data = venue.show_venue(venue_id, format_datetime)

  return render_template('pages/show_venue.html', venue=venue_data)


#=======================================================================#
#============================Create Venue===============================#
#-----------------------------------------------------------------------#

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])

def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  form = VenueForm(request.form)
  
  try:
    venue = Venue()
    form.populate_obj(venue)

    db.session.add(venue)
    db.session.commit()

    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')

  finally:
    db.session.close()

  return render_template('pages/home.html')


#======================================================================#
#========================== DELETE VENUE ==============================#

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None


#=======================================================================#
#=========================== Artists ===================================#
                # DISPLAY ALL ARTIST ON THE WEBPAGE
#-----------------------------------------------------------------------#


@app.route('/artists')

def artists():
  # TODO: replace with real data returned from querying the database
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)


#========================================================================#
#========================== SEARCH ARTIST ===============================#

@app.route('/artists/search', methods=['POST'])

def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  search_term=request.form.get('search_term', '')
  response = artist.search_artist(search_term)

  return render_template('pages/search_artists.html', results=response)



@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  
  data = artist.show_artist(artist_id, format_datetime)

  return render_template('pages/show_artist.html', artist=data)



#=================================================================#
#=========================UPDATE ARTIST===========================#
#=================================================================#

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])

def edit_artist(artist_id):

  form = ArtistForm()
  artist = Artist.query.get(artist_id)

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)



@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  form = ArtistForm()
  
  try:
    artist = Artist.query.get(artist_id)
    form.populate_obj(artist)
    db.session.commit()

    flash(f'Artist: {form.name.data} was updated successfully')

  except:

    db.session.rollback()
    flash(f'Artist {form.name.data} was not updated an Error Occurred')

  finally:
    db.session.close()


  return redirect(url_for('show_artist', artist_id=artist_id))


#=====================================================================#
#============================ EDIT VENUE =============================#


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])

def edit_venue(venue_id):

  form = VenueForm()
  venue = Venue.query.get(venue_id)

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))


#=================================================================
#                     CREATE ARTIST
#=================================================================


@app.route('/artists/create', methods=['GET'])

def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  form = ArtistForm(request.form)
  
  try:
    artist = Artist()
    form.populate_obj(artist)

    db.session.add(artist)
    db.session.commit()

    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')

  finally:
    db.session.close()

  return render_template('pages/home.html')


#================================================================#
#======================= SHOWS ==================================#
#             DISPLAY ALL SHOW ON THE WEBPAGE
#================================================================#

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.

  shows = Show.query.all()

  data = []

  for show in shows:

    data.append({
      "venue_id": show.venue.id,
      "venue_name":show.venue.name,
      "artist_id": show.artist.id,
      "artist_name": show.artist.name,
      "artist_image_link": show. artist.image_link,
      "start_time": str(show.start_time)
    })
  return render_template('pages/shows.html', shows=data)


#=========================================================#
#================== CREATE SHOW ==========================#

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])

def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  form = ShowForm()
  try:
    show = Show()
    form.populate_obj(show)
    db.session.add(show)
    db.session.commit()

    # on successful db insert, flash success
    flash('Show was successfully listed!')
  except:

    db.session.rollback()

    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Show could not be listed.')
  
  finally:
    db.session.close()

  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')


#=============================================================#
#================  ERROR HANDLERS  ===========================#
#=============================================================#

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
