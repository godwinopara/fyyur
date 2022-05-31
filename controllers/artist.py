from models import db, Artist
from datetime import datetime


#============================================
#           SEARCH ARTIST
#============================================

def search_artist(search_term):
    # Get user input from the search bar
    # Search the database for venue names that is similar to the user search input
    artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()

    response={
        "count": len(artists),
        "data": []
    }

    for artist in artists:
        response['data'].append({
        "id": artist.id,
        "name": artist.name,
    })

    return response



#============================================
#           SHOW AN ARTIST DETAILS
#============================================


def show_artist_details(Artist, Show, artist_id, format_datetime):

    # Get the artist_id which information will be displayed
    artist = Artist.query.get(artist_id)

    # Get the current time
    current_date = datetime.now()

    # Get the shows the artist have performed in and the venues
    artist_shows = Show.query.join('artist').join('venue').filter(Show.artist_id == artist_id)
    

    p_shows = [] # An array that hold past_shows
    u_shows = [] # An array that hold upcoming_shows

    # loop through all the shows the artist has performed in
    for show in artist_shows:
        
        if show.start_time < current_date:
            # added past shows to p_show list
            p_shows.append({
                "venue_id": show.id,
                "venue_name": show.venue.name,
                "venue_image_link": show.venue.image_link,
                "start_time": format_datetime(str(show.start_time))
            })
        else:
            # Add upcoming show to u_show list
            u_shows.append({
                "venue_id": show.id,
                "venue_name": show.venue.name,
                "venue_image_link": show.venue.image_link,
                "start_time": format_datetime(str(show.start_time))
            })

    return {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": p_shows,
    "upcoming_shows": u_shows,
    "past_shows_count": len(p_shows),
    "upcoming_shows_count": len(u_shows),
    }
