import logging
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

from profile_matcher_app.models import Campaign, PlayerProfile
from profile_matcher_app.serializers import CampaignSerializer, PlayerProfileSerializer

logger = logging.getLogger(__name__)

class GetPlayerProfile(APIView):
    def get(self, request, player_id):
        try:
            logger.info(f"starting Get playerprofile by id {player_id}")
            player = PlayerProfile.objects.get(player_id=player_id)
            serializer = PlayerProfileSerializer(player)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PlayerProfile.DoesNotExist:
            return Response({"error": "Player not found"}, status=status.HTTP_404_NOT_FOUND)

class GetCampaign(APIView):
    def get(self, request, campaign_id):
        try:
            logger.info(f"starting Get campaign by id {campaign_id}")
            campaign = Campaign.objects.get(campaign_id=campaign_id)
            serializer = CampaignSerializer(campaign)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Campaign.DoesNotExist:
            return Response({"error": "Campaign not found"}, status=status.HTTP_404_NOT_FOUND)
     
class GetClientConfig(APIView):
    def get(self, request, player_id):
        try:
            logger.info(f"Starting to get client config with id: {player_id}")
            player_profile = PlayerProfile.objects.get(player_id=player_id)

            campaigns = self.get_active_campaigns()
            logger.info(f"number of active campaigns: {len(campaigns)}")
            active_campaigns = []

            for campaign in campaigns:
                if self.does_player_match_campaign(player_profile, campaign):
                    active_campaigns.append(campaign.name)
                
                if active_campaigns:
                    self.update_player_profile(player_profile, active_campaigns)

                player_serialized = PlayerProfileSerializer(player_profile)

            return Response(player_serialized.data, status=status.HTTP_200_OK)
            
        except PlayerProfile.DoesNotExist:
            return Response({"error": "Player not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def get_active_campaigns(self):
        logger.info("Get campaigns that are active")
        return Campaign.objects.filter(
            enabled=True,
            start_date__lte=datetime.now(),
            end_date__gte=datetime.now()
        )

    def does_player_match_campaign(self, player_profile, campaign):
        logger.info("Check if the player matches the conditions for the campaign")
        match = True
        matchers = campaign.matchers

        if 'level' in matchers:
            if not (matchers['level']['min'] <= player_profile.level <= matchers['level']['max']):
                match = False

        if 'has' in matchers:
            if 'country' in matchers['has'] and player_profile.country not in matchers['has']['country']:
                match = False
            if 'items' in matchers['has'] and not any(item in player_profile.inventory for item in matchers['has']['items']):
                match = False

        if 'does_not_have' in matchers:
            if 'items' in matchers['does_not_have'] and any(item in player_profile.inventory for item in matchers['does_not_have']['items']):
                match = False

        logger.info(f"Campaign {campaign.campaign_id} is match: {match}")
        return match

    def update_player_profile(self, player_profile, active_campaigns):
        logger.info("Update the player's profile with the active campaigns")
        player_profile.active_campaigns = list(set(player_profile.active_campaigns + active_campaigns))
        player_profile.save()