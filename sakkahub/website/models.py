from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone
from django.contrib.auth.models import User as Individual
import datetime
import random
from django.core.validators import MaxValueValidator, MinValueValidator

CHOICES = (
    (1, _("Under 10")),
    (2, _("Under 15")),
    (3, _("Under 20")),
)


class AccessLevel(models.IntegerChoices):
    Player = 0
    Parent = 1
    Volunteer = 2
    Medical = 3
    Coach = 4
    Clubs = 5
    Referee = 6
    Organizer = 7
    Director = 8


class Individuals(models.Model):
    id = models.AutoField(primary_key=True)
    individual = models.OneToOneField(Individual, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
    individual_level = models.IntegerField(choices=AccessLevel.choices, default=0)
    date_of_birth = models.DateField(default= timezone.now)


class Match(models.Model):
    team1 = models.CharField(max_length=100)
    team2 = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=100)
    content = models.TextField()
    team = models.ForeignKey(Individual, on_delete=models.CASCADE)

class MatchDetails(models.Model):
    team1 = models.CharField(max_length=100)
    team2 = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=100)
    content = models.TextField()
    match_result = models.CharField(max_length=10, default='NA')
    team1_score = models.IntegerField(default=0)
    team2_score = models.IntegerField(default=0)
    team1_sc = models.CharField(max_length=10)
    team2_sc = models.CharField(max_length=10) 
    team = models.ForeignKey(Individual, on_delete=models.CASCADE)

class Match_Result(models.Model):
    match_id = models.ForeignKey(Match, on_delete=models.CASCADE)
    match_result = models.CharField(max_length=10)
    team1_score = models.IntegerField(default=0)
    team2_score = models.IntegerField(default=0)
    team1_sc = models.CharField(max_length=10)
    team2_sc = models.CharField(max_length=10)    

class TeamList(models.Model):
    team_name = models.CharField(max_length=100)
    no_of_players = models.IntegerField()
    
class Matches(models.Model):
    match_id = models.CharField(max_length=10)
    ground_name = models.CharField(max_length=100)
    pitch_number = models.IntegerField(default=0)
    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    refree_name1 = models.CharField(max_length=20)
    date_time = models.DateTimeField(default=timezone.now)
    tournament_id = models.CharField(max_length=10, default="random")
    touranment_name = models.CharField(max_length=100, default="random_tournament")
    tournament_start_date = models.DateTimeField(default=timezone.now)
    tournament_end_date = models.DateTimeField(default=timezone.now)

    
class TeamIndividuals(models.Model):
    id = models.AutoField(primary_key=True)
    # individual = models.OneToOneField(Individual, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
    individual_level = models.IntegerField(choices=AccessLevel.choices, default=0)
    date_of_birth = models.DateField(default= timezone.now)
    team_name = models.CharField(max_length=200)
    coach_name = models.CharField(max_length=200)

    def __str__(self):
        return self.team_name


class Team(models.Model):
    team_name = models.CharField(max_length=50)
    no_of_players = models.PositiveIntegerField(null=True, blank= True, validators=[MaxValueValidator(15)])
    age_category = models.IntegerField(choices=CHOICES, default=1)

    def __str__(self):
        return self.team_name


class Players(models.Model):
    player_name = models.CharField(max_length=50)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.player_name


class Coaches(models.Model):
    coach_name = models.CharField(max_length=50)
    phone_number = models.BigIntegerField(unique=True, null=True)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.coach_name


class Team_manager(models.Model):
    manager_name = models.CharField(max_length=50)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    phone_number = models.BigIntegerField(unique=True)
    email = models.EmailField(null=True, max_length=255, unique=True, db_index=True, verbose_name=_('email address'))

    def __str__(self):
        return self.manager_name


class Inventory(models.Model):
    item_name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    state = models.CharField(max_length=20)
    vendor_name = models.CharField(max_length=40)

