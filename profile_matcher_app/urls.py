from django.urls import path

from profile_matcher_app.views import GetPlayerProfile


urlpatterns = [
    path('get_client_config/<uuid:player_id>/', GetPlayerProfile.as_view(), name='get_player_profile'),
]
