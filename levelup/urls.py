from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from levelupapi.views import register_user, login_user, GameTypeView, GameView, EventView, GamerView, user_profile
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'gametypes', GameTypeView, 'gametype')
router.register(r'games', GameView, 'game')
router.register(r'events', EventView, 'event')
router.register(r'gamer', GamerView, 'gamer')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('levelupreports.urls')),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('profile', user_profile),

]
