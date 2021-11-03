"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from levelupapi.models import Gamer
from levelupapi.views.user import UserSerializer



class GamerView(ViewSet):
    """Level up game types"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        try:
            gamer = Gamer.objects.get(pk=pk)
            serializer = GamerSerializer(gamer, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        gamer = Gamer.objects.get(user=request.auth.user)

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = GamerSerializer(
            gamer, many=False, context={'request': request})
        return Response(serializer.data)

class GamerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Gamer
        fields = ['user']
