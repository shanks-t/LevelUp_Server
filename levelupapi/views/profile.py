from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import serializers

from django.contrib.auth.models import User
from django.db.models import F


from levelupapi.models import Event, Gamer, Game, GameType, EventGamer

@api_view(['GET'])
def user_profile(request):
    """Handle GET requests to profile resource

    Returns:
        Response -- JSON representation of user info and events
    """
    gamer = Gamer.objects.get(user=request.auth.user)
    events = Event.objects.all()
    # TODO: Use the django orm to filter events if the gamer is attending the event
    # attending = 
    attending = events.filter(attendees__id=gamer.id)
    # TODO: Use the orm to filter events if the gamer is hosting the event
    # hosting =
    hosting = events.filter(organizer__id=gamer.id)

    attending = EventSerializer(
        attending, many=True, context={'request': request})
    hosting = EventSerializer(
        hosting, many=True, context={'request': request})
    gamer = GamerSerializer(
        gamer, many=False, context={'request': request})

    # Manually construct the JSON structure you want in the response
    profile = {
        "gamer": gamer.data,
        "attending": attending.data,
        "hosting": hosting.data
    }

    return Response(profile)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for gamer's related Django user"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class GamerSerializer(serializers.ModelSerializer):
    """JSON serializer for gamers"""
    user = UserSerializer(many=False)

    class Meta:
        model = Gamer
        fields = ('user', 'bio')


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    class Meta:
        model = Game
        fields = ('title',)


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""
    game = GameSerializer(many=False)

    class Meta:
        model = Event
        fields = ('id', 'game', 'description', 'date', 'time')
