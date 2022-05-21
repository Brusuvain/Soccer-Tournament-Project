from django.contrib import admin
from .models import Individuals, Team, Players, Coaches, Team_manager, Match, MatchDetails, Match_Result, TeamList


admin.site.register(Individuals)
admin.site.register(Team)
admin.site.register(Players)
admin.site.register(Coaches)
admin.site.register(Team_manager)
admin.site.register(Match)
admin.site.register(Match_Result)
admin.site.register(MatchDetails)
admin.site.register(TeamList)
