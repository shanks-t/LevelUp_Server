"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from levelupapi.models import Event, Gamer, Game, GameType
from levelupapi.views.gamer import GamerSerializer


class EventView(ViewSet):
    """Level up games"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """


        attendees = Event.objects.get(pk=request.data["anttendees"])
        organizer = Event.objects.get(pk=request.data["organizer"])

        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request
        try:
            # Create a new Python instance of the Game class
            # and set its properties from what was sent in the
            # body of the request from the client.
            event = Event.objects.create(
                game=request.data["game"],
                organizer=organizer,
                description=request.data["description"],
                date=request.data["date"],
                time=request.data["time"],
                attendees=attendees
            )
            serializer = Eventserializer(event, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/games/2
            #
            # The `2` at the end of the route becomes `pk`
            event = Event.objects.get(pk=pk)
            serializer = Eventserializer(event, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`
        event = Event.objects.get(pk=pk)
        event.game = request.data["game"]
        event.organizer = request.data["organizer"]
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.time = request.data["time"]
        event.attendees = request.data["attendees"]

        event.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            event = Event.objects.get(pk=pk)
            event.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """
        # Get all game records from the database
        events = Event.objects.all()

        # Support filtering games by type
        #    http://localhost:8000/games?type=1
        #

        serializer = Eventserializer(
            events, many=True, context={'request': request})
        return Response(serializer.data)

class Eventserializer(serializers.ModelSerializer):
    organizer = GamerSerializer()
    
    class Meta:
        model = Event
        fields = ['id', 'game', 'organizer', 'description', 'date', 'time', 'attendees']
