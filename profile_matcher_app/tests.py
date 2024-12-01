from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from profile_matcher_app.models import PlayerProfile, Campaign
from datetime import datetime

class GetClientConfigTest(TestCase):
    def setUp(self):

        self.playerprofile = PlayerProfile.objects.create(
            player_id='d6b219cd-1116-4884-b977-85e028c8c193',
            credential='apple_credential',
            created="2023-01-10T13:37:17Z",
            modified="2023-01-23T13:37:17Z",
            last_session="2023-01-23T13:37:17Z",
            total_spend=400,
            total_refund=0,
            total_transactions=5,
            last_purchase="2023-02-22T13:37:17Z",
            active_campaigns=[],
            devices=[{
                "id": 1,
                "model": "iphone 11",
                "carrier": "vodafone",
                "firmware": "123"
            }],
            level=3,
            xp=1000,
            total_playtime=144,
            country="CA",
            language="fr",
            birthdate="2000-01-10T13:37:17Z",
            gender="male",
            inventory={
                "cash": 123,
                "coins": 123,
                "item_1": 1,
                "item_34": 3,
                "item_55": 2
            },
            clan={
                "id": 123456,
                "name": "Hello world clan"
            },
            custom_field="mycustom"
        )
        
        self.campaign1 = Campaign.objects.create(
            campaign_id="07a77daf-0e24-44ae-bf23-80ccbe553e57",
            game="testgame",
            name= "test_campaign",
            priority=10.5,
            matchers={
                "level": {"min": 1, "max": 3},
                "has": {"country": ["CA"], "items": ["item_1"]},
                "does_not_have": {"items": ["item_4"]}
            },
            start_date="2024-01-25T00:00:00Z",
            end_date="2025-02-25T00:00:00Z",
            enabled=True,
            last_updated="2024-07-13T11:46:58Z"
        )
        
        self.campaign2 = Campaign.objects.create(
            campaign_id="bb6ca0b1-e1f9-4f40-bbe0-e9758200030d",
            game="testgame",
            name="another_campaign",
            priority=5.5,
            matchers={
                "level": {"min": 1, "max": 3},
                "has": {"country": ["US"], "items": ["item_1"]},
                "does_not_have": {"items": ["item_4"]}
            },
            start_date="2024-01-25T00:00:00Z",
            end_date="2025-02-25T00:00:00Z",
            enabled=True,
            last_updated="2024-07-13T11:46:58Z"
        )
        
        self.client = APIClient()

    def test_get_player_profile(self):
        """ Verify the player profile exists """
        response = self.client.get(f'/api/playerprofiles/{self.playerprofile.player_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_campaign_profile(self):
        """ Verify the campaign exists """
        response = self.client.get(f'/api/campaigns/{self.campaign1.campaign_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_client_config_with_matching_campaign(self):
        """ TEST 1 Verify the player is assigned with the correct campaign """
        response = self.client.get(f'/api/get_client_config/{self.playerprofile.player_id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        player_profile = PlayerProfile.objects.get(pk=self.playerprofile.player_id)
        self.assertIn("test_campaign", player_profile.active_campaigns)
        
    def test_get_client_config_with_no_matching_campaign(self):
        """ TEST 2 Verify that player is NOT assigned with unmatching campaign """
        self.playerprofile.level = 5
        self.playerprofile.save()
        
        response = self.client.get(f'/api/get_client_config/{self.playerprofile.player_id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        player_profile = PlayerProfile.objects.get(pk=self.playerprofile.player_id)
        self.assertEqual(player_profile.active_campaigns, [])
    
    def test_get_client_config_with_duplicate_campaign(self):
        """ TEST 3 Verify the campaigns are not duplicated """
        self.client.get(f'/api/get_client_config/{self.playerprofile.pk}')
        
        response = self.client.get(f'/api/get_client_config/{self.playerprofile.player_id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        player_profile = PlayerProfile.objects.get(pk=self.playerprofile.player_id)
        self.assertEqual(player_profile.active_campaigns.count("test_campaign"), 1)

