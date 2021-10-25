from message_in_a_bottle.api.models import Story
from message_in_a_bottle.api.services import MapService

class MapFacade():
  def get_stories(latitude, longitude):
    response = MapService.get_stories(latitude, longitude, Story.map_stories())
    results = [] if response['resultsCount'] == 0 else response['searchResults']
    city_state = MapService.get_city_state(latitude, longitude)
    return [results, city_state]