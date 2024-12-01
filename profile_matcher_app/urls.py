from django.urls import path

from profile_matcher_app.views import GetCampaign, GetClientConfig, GetPlayerProfile


urlpatterns = [
    path('playerprofiles/<uuid:player_id>/', GetPlayerProfile.as_view(), name='get_player_profile'),
    path('campaigns/<uuid:campaign_id>/', GetCampaign.as_view(), name='get_campaign'),
    path('get_client_config/<uuid:player_id>/', GetClientConfig.as_view(), name='get_client_config')
]
