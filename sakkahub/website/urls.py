from django.urls import path
from . import views
from .views import MatchListView, MatchDetailView, MatchCreateView


urlpatterns = [
    path('', views.home, name='website-home'),
    path('register/', views.registration_page, name='register'),
    path('LiveTournaments/', views.getLiveTournaments, name='LiveTournaments'),
    path('volunteer/', views.getVolunteerPage, name='website-volunteer'),
    path('referee/', views.getRefreePage, name='website-refree'),
    path('maps/', views.getMapPage, name='maps'),

    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_button, name='logout'),

    path('edit/<int:user_id>/', views.edit_details, name='edit-user'),
    path('register-team/', views.teamregister, name='register-team'),

    path('team-squad/', views.teamsquad, name='team-squad'),
    path('website/team-details/<str:team_id>', views.teamdetails, name='team-details'),
    # path('team_update/', views.team_update, name='team_update'),
    path('website/delete_player/<str:pk>', views.delete_player, name="delete_player"),
    path('website/coach_update/<int:pk>', views.coach_update, name='coach_update'),
    path('contact/', views.contact, name='contact'),
   
    path('refree/', views.getRefreePage, name='website-refree'),
    path('maps/',views.getMapPage,name='maps'),
    path('inventory/', views.getInventory, name='inventory'),
    path('inventory/items', views.addInventoryItems, name='add-items-to-inventory'),

    path('schedule/', MatchListView.as_view(), name='match-schedule'),
    path('pointtable/', views.displayPointTable, name='tournament-point-table'),
    path('match/<int:pk>/', MatchDetailView.as_view(), name='match-detail'),
    path('match/matchresult/', views.matchResult, name='match-result'),
    path('addteam/', MatchCreateView.as_view(), name='match-create'),
    path('addteam_home/', views.addTeamHome, name = 'addteam-home'),
    path('matchreport/', views.matchReport, name='match-report'),
    path('medicalstaffdetails/', views.medicalStaffDetails, name='medical-staff-details'),
    path('events/',views.getEventPage,name='events'),
    path('fields/', views.getFieldsPage,name='field-info'),


]

