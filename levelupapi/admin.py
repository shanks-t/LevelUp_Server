from django.contrib import admin
from levelupapi.models import Game, Event, Gamer, GameType

# Register your models here.
admin.site.register(Game)
admin.site.register(Event)
admin.site.register(Gamer)
admin.site.register(GameType)