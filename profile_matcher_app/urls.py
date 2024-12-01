from django.urls import path

from profile_matcher_app.views import GetCampaign, GetPlayerProfile


urlpatterns = [
    path('get_client_config/<uuid:player_id>/', GetPlayerProfile.as_view(), name='get_player_profile'),
    path('campaigns/<uuid:campaign_id>/', GetCampaign.as_view(), name='get_campaign'),
]
