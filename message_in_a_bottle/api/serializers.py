from rest_framework import serializers
from .models import Story

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['id', 'latitude', 'longitude', 'message', 'name', 'title', 'location', 'created_at', 'updated_at']

    def stories_index_serializer(response):
        stories = map(StorySerializer.reformat_mapquest_response, response)
        dict = {
            'input_location': 'This is a temporary location!',
            'stories': list(stories)
        }
        return dict

    def reformat_mapquest_response(story):
        if story:
            return {
                'id': story['key'],
                'type': 'story',
                'attributes': {
                    'title': story['name'],
                    'distance_in_miles': story['distance'],
                    'latitude': story['shapePoints'][0],
                    'longitude': story['shapePoints'][1]
                }
            }

    def reformat(self, story):
        return {
            'id': story['id'],
            'type': 'Story',
            'attributes': {
                'name': story['name'],
                'title': story['title'],
                'message': story['message'],
                'latitude': story['latitude'],
                'longitude': story['longitude'],
                'location': story['location'],
                'created_at': story['created_at'],
                'updated_at': story['updated_at']
            }
        }

    def story_directions_serializer(response, story):
        if response['routeError']['errorCode'] == 2:
            return {'message': 'Impossible route.'}
        else:
            directions = map(StorySerializer.format_directions, response['legs'][0]['maneuvers'])
            return list(directions)

    def format_directions(maneuver):
        return {
            'id': None,
            'type': 'directions',
            'attributes': {
                'narrative': maneuver['narrative'],
                'distance': f"{maneuver['distance']} miles",
            }
        }

     def coordinates_error(self):
            return {
                'coordinates': [
                    'Invalid latitude or longitude.'
                ]
            }
