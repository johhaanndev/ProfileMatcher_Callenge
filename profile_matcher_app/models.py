from django.db import models

class Campaign(models.Model):
    campaign_id = models.UUIDField(primary_key=True)
    game = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    priority = models.FloatField()
    matchers = models.JSONField()
    enabled = models.BooleanField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    last_updated = models.DateTimeField()

    def __str__(self):
        return f"Campaign {self.campaign_id}"

class PlayerProfile(models.Model):
    player_id = models.UUIDField(primary_key=True)
    credential = models.CharField(max_length=50)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    last_session = models.DateTimeField()
    total_spend = models.FloatField()
    total_refund = models.FloatField()
    total_transactions = models.IntegerField()
    last_purchase = models.DateTimeField()
    active_campaigns = models.JSONField(default=list)
    devices = models.JSONField(default=list)
    level = models.IntegerField()
    xp = models.IntegerField()
    total_playtime = models.FloatField()
    country = models.CharField(max_length=20)
    language = models.CharField(max_length=20)
    birthdate = models.DateTimeField()
    gender = models.CharField(max_length=10)
    inventory = models.JSONField(default=dict)
    clan = models.JSONField(default=dict)
    custom_field = models.CharField(max_length=50)

    def __str__(self):
        return f"Player {self.player_id}"