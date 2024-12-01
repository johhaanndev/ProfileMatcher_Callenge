from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from profile_matcher_app.models import Campaign, PlayerProfile
from profile_matcher_app.serializers import CampaignSerializer, PlayerProfileSerializer

class GetPlayerProfile(APIView):
    def get(self, request, player_id):
        try:
            player = PlayerProfile.objects.get(player_id=player_id)
            serializer = PlayerProfileSerializer(player)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PlayerProfile.DoesNotExist:
            return Response({"error": "Player not found"}, status=status.HTTP_404_NOT_FOUND)
        
class GetCampaign(APIView):
    def get(self, request, campaign_id):
        try:
            campaign = Campaign.objects.get(campaign_id=campaign_id)
            serializer = CampaignSerializer(campaign)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Campaign.DoesNotExist:
            return Response({"error": "Campaign not found"}, status=status.HTTP_404_NOT_FOUND)