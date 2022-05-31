from flask import request
from models import Show, Venue
from datetime import datetime


def venue():
  # Get all the venues from the database
    venues = Venue.query.all()

    # Get the state and city and remove duplicates
    unique_venues = Venue.query.distinct(Venue.city, Venue.state).all()

    data = [] # An array where the data that will be passed to the view is stored

    current_time = datetime.now()

    for unique_venue in unique_venues:

        venue_data = [] # An array that stores all the venues in each city

        for venue in venues:

            if unique_venue.city == venue.city:

                venue_data.append({
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": len([Show.query.filter(Show.start_time > current_time)])
                })
        data.append({
        "city": unique_venue.city,
        "state": unique_venue.state,
        "venues": venue_data
        })


    return data



#----------------------------------------------------------#
#----------------------------------------------------------#
#      SEARCH VENUE
#----------------------------------------------------------#

def search_venue():
    # Get user input from the search bar
    search_term=request.form.get('search_term', '')

    # Search the database for venue names that is similar to the user search input
    venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()

    response={
        "count": len(venues),
        "data": []
    }

    for venue in venues:
        response['data'].append({
        "id": venue.id,
        "name": venue.name,
    })

    return response



#============================================================#
#           SHOW VENUE
#============================================================#

def show_venue(venue_id, format_datetime):

  # Get the Venue id that its information will be displayed 
    venues = Venue.query.get(venue_id)

    # Get the current time
    current_time = datetime.today()


    # Get all the venues where a show has been performed
    shows = Show.query.filter(Show.venue_id == venue_id)


    past_shw = [] # An array that hold all the past shows
    upcoming_shw = [] # An array that hold all upcoming shows

    # Loop Through every row in the Show Model table
    for show in shows:
        
            if show.start_time > current_time:
            # put the shows that are upcoming to the upcoming_show array
                upcoming_shw.append({
                    "artist_id": show.artist.id,
                    "artist_name": show.artist.name,
                    "artist_image_link": show.artist.image_link,
                    "start_time": format_datetime(str(show.start_time))
                })
            else:
                # put the show that already took place in the past_shows array
                past_shw.append({
                    "artist_id": show.artist.id,
                    "artist_name": show.artist.name,
                    "artist_image_link": show.artist.image_link,
                    "start_time": format_datetime(str(show.start_time))
                })


    return {
    "id": venues.id,
    "name": venues.name,
    "genres": venues.genres,
    "city": venues.city,
    "state": venues.state,
    "phone": venues.phone,
    "website": venues.website,
    "facebook_link": venues.facebook_link,
    "seeking_talent": venues.seeking_talent,
    "seeking_description": venues.seeking_description,
    "image_link": venues.image_link,
    "past_shows": past_shw,
    "upcoming_shows": upcoming_shw,
    "past_shows_count": len(past_shw),
    "upcoming_shows_count": len(upcoming_shw),
    }