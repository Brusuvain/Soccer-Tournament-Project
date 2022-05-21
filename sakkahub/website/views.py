
from django import forms
from django.contrib.auth import login, authenticate, logout, forms as auth_forms
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Individuals, Individual, Matches, TeamIndividuals, Inventory, AccessLevel
from django.template.response import TemplateResponse
from django.http import HttpResponse, Http404
from django.core import serializers
from django.views.generic import ListView, DetailView, CreateView
from .models import Match, TeamList, MatchDetails
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Individuals, Individual, Team, Players, Coaches, Team_manager
from django.forms import formset_factory
from django.forms import modelformset_factory
from django.forms import MultiWidget, TextInput
from django.contrib import messages
from django.shortcuts import (get_object_or_404, render,HttpResponseRedirect)
from django.http import Http404
from django.utils.translation import ugettext_lazy as _



def current_user(request, required_auth=AccessLevel.Player):
    if request.user.is_authenticated:
        user = Individual.objects.get(username=request.user)
    else:
        return None

    return user


def home(request):
    return TemplateResponse(request, 'website/home.html', {})


def pickup_individual(role, time):
    individualInfo = json.loads(serializers.serialize("json", Individuals.objects.filter(individual_level=role)))  
    for info in individualInfo:
        information = info['fields']
        name = information['firstname']
        role = information['individual_level']
        if role == 2:
            matchesDetails = json.loads(serializers.serialize("json", Matches.objects.filter(volunteer_name=name)))
        if role == 3:
            matchesDetails = json.loads(serializers.serialize("json", Matches.objects.filter(medical_practicner_name=name)))
        if role == 6:
            matchesDetails = json.loads(serializers.serialize("json", Matches.objects.filter(refree1_name=name)))
        datetime = matchesDetails['date_time']

class CreateIndividualForm(auth_forms.UserCreationForm):
    class Meta:
        model = Individual
        fields = ['first_name', 'last_name', 'email', 'username']

    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()


class CreateIndividualsForm(forms.ModelForm):
    class Meta:
        model = Individuals
        fields = ('address', 'phone', 'date_of_birth')

    address = forms.CharField(widget=forms.Textarea)
    date_of_birth = forms.DateTimeInput()
    phone = forms.CharField()


def registration_page(request):
    form1 = CreateIndividualForm(request.POST)
    form2 = CreateIndividualsForm(request.POST)
    if form1.is_valid() & form2.is_valid():
        form1.save()
        if form2.is_valid():
            form2.save()
        return redirect('website-home')
    else:
        form1 = CreateIndividualForm()
        form2 = CreateIndividualsForm()

    return TemplateResponse(request, 'website/registration_page.html', {'form1': form1, 'form2': form2})



def getVolunteerPage(request):
    # This data should come from databse table.
    # For now it is hardcoded.
    meetings = [
                    {
                        'title': 'Futsal Riverside Tournament (Lambda Sponser)',
                        'start': '2021-09-09',
                        'end': '2021-09-11'
                    },
                    {
                        'title': 'Hayden Ground',
                        'start': '2021-09-09T10:30:00',
                        'end': '2021-09-09T12:30:00'
                    },
                    {
                        'title': 'Bernabeu Stands',
                        'start': '2021-09-09T14:30:00',
                        'end': '2021-09-09T16:30:00'
                    },
                    {
                        'title': 'Hayden Ground',
                        'start': '2021-09-10T10:30:00',
                        'end': '2021-09-10T12:30:00'
                    },
                    {
                        'title': 'Troll Football Championship',
                        'start': '2021-09-03',
                        'end': '2021-09-07'
                    },
                    {
                        'title': 'Eden Stadium',
                        'start': '2021-09-21T17:30:00',
                        'end': '2021-09-21T19:30:00'
                    },
                    {
                        'title': 'Eden Stadium',
                        'start': '2021-09-21T11:30:00',
                        'end': '2021-09-21T12:30:00'
                    },
                    {
                        'title': 'Eden Stadium',
                        'start': '2021-09-21T14:30:00',
                        'end': '2021-09-21T16:30:00'
                    },
                    {
                        'title': 'Hayden Ground',
                        'start': '2021-09-05T03:30:00',
                        'end': '2021-09-05T05:30:00'
                    },
                    {
                        'title': 'Bernabeu Stand',
                        'start': '2021-09-05T10:30:00',
                        'end': '2021-09-05T12:30:00'
                    },
                     {
                        'title': 'Summer Tournament',
                        'start': '2021-09-20',
                        'end': '2021-09-25'
                    },
                ]
    meetingSet = json.dumps(meetings)        
    return render(request, 'pages/volunteer.html',{'events': meetingSet})


def getMapPage(request):
    return render(request,'pages/maps.html')

def getRefreePage(request):
    # This data should come from databse table.
    # For now it is hardcoded.
    matches = Matches.objects.all()
    matchSets = serializers.serialize("json", matches)       
    return render(request, 'pages/referee.html',{'matchSchedule': matchSets})


def medicalStaffDetails(request):
    return render(request, 'schedule/MedicalStaffDetails.html')

def getLiveTournaments(request):
    matches = Matches.objects.all()
    matchSets = serializers.serialize("json", matches)       
    return render(request, 'pages/LiveTournaments.html',{'matchSchedule': matchSets})

def getInventory(request):
    inventory = Inventory.objects.all()
    inventorySet = serializers.serialize("json", inventory)  
    return render(request, 'pages/inventory.html',{'inventoryDetails': inventorySet})

# Rest APIs, these function is for handling CRUD Operations

@csrf_exempt
def getInventoryItems(request):
    inventory = Inventory.objects.all()
    inventorySet = serializers.serialize("json", inventory)  
    return HttpResponse(inventorySet, content="text/json")

@csrf_exempt
def addInventoryItems(request):
    #payload = json.loads(request.body)
  
    payload = str(request.body)
    payload = payload.split("'")[1]
    payloads_values = payload.split("&")
    itemName = str(payloads_values[0].split("=")[1])
    itemName = itemName.replace("+"," ")
    quantity = int(payloads_values[1].split("=")[1])
    vendorName = str(payloads_values[2].split("=")[1])
    vendorName = vendorName.replace("+"," ")
    print(vendorName)
    if itemName == "" :
        return HttpResponse("ITEM NAME WAS NOT ENTERED")
    if vendorName == "":
        return HttpResponse("VENDOR NAME WAS NOT ENTERED")
    if quantity < 15:
        criticality = "Immediate Order Required"
    if quantity == 0:
        criticality = "Out Of Stock"
    if quantity > 15 and quantity<35:
        criticality = "Item is soon going to be out of stock"
    if quantity >  35:
        criticality = "Item Available in Stock"

    updated_rows = Inventory.objects.filter(item_name=itemName).update(quantity=quantity, state=criticality, vendor_name=vendorName)
    if not updated_rows:
        Inventory.objects.create(item_name=itemName, quantity=quantity, state=criticality, vendor_name=vendorName)
    
    #Inventory.objects.create(item_name=itemName, quantity=quantity, state=criticality, vendor_name=vendorName)
    return HttpResponse("ORDER PLACED SUCCESSFULLY")


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


def login_page(request):
    form = LoginForm(request.POST)
    user = None

    if form.is_valid():
        user1 = authenticate(request,
                             username=form.cleaned_data['username'],
                             password=form.cleaned_data['password'])
        try:
            user = Individuals.objects.get(individual=user1)
            if user is None:
                form.add_error(None, "Username or password is incorrect")
            else:
                login(request, user.individual)
                return TemplateResponse(request, 'website/home.html', {})
        except Individuals.DoesNotExist as exception:
            raise Http404("No such User") from exception

    return TemplateResponse(request, 'website/login.html', {
        'form': form
    })


def logout_button(request):
    logout(request)
    return TemplateResponse(request, 'website/home.html', {})


class NameForm(forms.ModelForm):
    class Meta:
        model = Individual
        fields = {'first_name', 'last_name'}

    first_name = forms.CharField()
    last_name = forms.CharField()


class EmailForm(forms.ModelForm):
    class Meta:
        model = Individual
        fields = {'email'}

    email = forms.EmailField()


class AddressForm(forms.ModelForm):
    class Meta:
        model = Individuals
        fields = {'address'}

    address = forms.CharField()


class PhoneForm(forms.ModelForm):
    class Meta:
        model = Individuals
        fields = {'phone'}

    phone = forms.CharField()


def matchSchedule(request):
    #return HttpResponse('<h1>Match Schedule Page</h1>')
    context = {
        'posts': MatchDetails.objects.all()
    }
    return render(request,'schedule/MatchSchedule.html' , context)

class MatchListView(ListView):
    model = MatchDetails
    template_name = 'schedule/MatchSchedule.html'
    context_object_name = 'posts'

class MatchDetailView(DetailView):
    model = MatchDetails

class MatchCreateView(SuccessMessageMixin,CreateView):
    model = TeamList
    fields = ['team_name', 'no_of_players']
    success_url = reverse_lazy('addteam-home')
    success_message = 'New Team added to Tournament'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return super().get_success_url(self)

def addTeam(request):
    #return HttpResponse('<h1>Add team to be scheduled</h1>')
    return render(request,'schedule/AddTeam.html' , {'title': 'Soccer League'})

def matchReport(request):
    return render(request, 'schedule/MatchReport.html')

def matchResult(request):
    return render(request, 'schedule/MatchResult.html')

def medicalStaffDetails(request):
    return render(request, 'schedule/MedicalStaffDetails.html')

def displayPointTable(request):
    return render(request, 'schedule/TournamentPointTable.html')

def addTeamHome(request):
    return render(request, 'schedule/AddTeamHome.html')

fields=[{
    'stadium':'Gillete Stadium',
    'fieldimg':'https://static.clubs.nfl.com/image/private/f_auto/ravens/sfcbkxaiv4lvpsib4bsc'
},
{
    'stadium':'LA Galaxy',
    'fieldimg':'https://images.mlssoccer.com/image/private/t_keep-aspect-ratio-e-mobile/f_auto/mls-lag-prd/zfpkmhlil95sbapuwb1w.jpg'
},
{
    'stadium':'Sun Devil Stadium',
    'fieldimg':'https://www.rateyourseats.com/assets/images/seating_charts/static/arizona-state-football-seating-chart-at-sun-devil-stadium.jpg'
}]

eventDetails = [
    {
        'home_team': 'The Red Devils',
        'away_team': 'Arsenal Gunners',
        'tournament_name':'Under 18 Boys & Girls',
        'tournament_id': '1',
        'tournament_start_date': '11-24-2021',
        'tournament_end_date': '11-24-2021',
        'event_start_date': '11-24-2021',
        'event_end_date': '11-24-2021',
        'Match_date':'11-24-2021',
        'Match_timing': '19:30',
        'venue': 'Rose Bowl Stadium',
        'match_id': '1'
    },
    {
        'home_team': 'Arsenal Gunners',
        'away_team': 'FC Santa Claus',
        'tournament_name':'Under 18 Boys & Girls',
        'tournament_id': '1',
        'tournament_start_date': '11-26-2021',
        'tournament_end_date': '11-27-2021',
        'event_start_date': '11-24-2021',
        'event_end_date': '11-24-2021',
        'Match_date':'11-26-2021',
        'Match_timing': '19:30',
        'venue': 'Gillette Stadium',
        'match_id': '2'
    },
    {
        'home_team': 'FC Santa Claus',
        'away_team': 'Club Always Ready',
        'tournament_name':'Under 25 Boys & Girls',
        'tournament_id': '2',
        'tournament_start_date': '10-20-2021',
        'tournament_end_date': '10-24-2021',
        'event_start_date': '11-24-2021',
        'event_end_date': '11-24-2021',
        'Match_date':'10-24-2021',
        'Match_timing': '00:30',
        'venue': 'Old Trafford Stadium',
        'match_id': '3'
    },
    {
        'home_team': 'Eliminator winning team',
        'away_team': 'Qualifier winning team',
        'tournament_name':'Under 25 Boys & Girls',
        'tournament_id': '2',
        'tournament_start_date': '10-20-2021',
        'tournament_end_date': '10-24-2021',
        'event_start_date': '11-24-2021',
        'event_end_date': '11-24-2021',
        'Match_date':'10-24-2021',
        'Match_timing': '11:30',
        'venue': 'Gillete Stadium',
        'match_id': '4'
    }
]
def getEventPage(request):
    context = {
        'events': eventDetails
    }
    return render(request,'pages/events.html',context)

def getFieldsPage(request):
    stadiums = {
'fields':fields
    }
    return render(request,'pages/fieldInfoPage.html',stadiums)
def edit_details(request, user_id):
    user = current_user(request)
    try:
        user_edited = Individuals.objects.get(individual_id=user_id)
    except Individuals.DoesNotExist as exception:
        raise Http404("No such User") from exception

    original_email = user_edited.individual.email
    original_fname = user_edited.individual.first_name
    original_lname = user_edited.individual.last_name
    original_address = user_edited.address
    original_phone = user_edited.phone
    print(original_email, original_fname, original_lname)

    if user != user_edited.individual:
        raise Http404("Cannot edit this user")

    form_address = AddressForm(request.POST, instance=user_edited)
    form_phone = PhoneForm(request.POST, instance=user_edited)
    form_name = NameForm(request.POST, instance=user_edited.individual)
    form_email = EmailForm(request.POST, instance=user_edited.individual)

    if form_address.is_valid() and form_address.cleaned_data['address'] != original_address:
        form_address.save()
    else:
        form_address = AddressForm(instance=user_edited)

    if form_phone.is_valid() and form_phone.cleaned_data['phone'] != original_phone:
        form_phone.save()
    else:
        form_phone = PhoneForm(instance=user_edited)

    if form_email.is_valid() and form_email.cleaned_data['email'] != original_email:
        form_email.save()
    else:
        form_email = EmailForm(instance=user_edited.individual)

    if form_name.is_valid() and (form_name.cleaned_data['first_name'] != original_fname
                                 or form_name.cleaned_data['last_name'] != original_lname):
        form_name.save()
        print(form_name.cleaned_data['first_name'])
    else:
        form_name = NameForm(instance=user_edited.individual)
       
    return TemplateResponse(request, 'website/edit_details.html', {
        'form_name': form_name,
        'form_email': form_email,
        'form_phone': form_phone,
        'form_address': form_address
    })


class CreateTeamIndividualForm(forms.ModelForm):
    class Meta:
        model = Individual
        fields = ['team_name', 'coach_name', 'email', 'team_id', 'password', 'number_of_players_in_squad']

    team_name = forms.CharField()
    coach_name = forms.CharField()
    email = forms.EmailField()
    team_id = forms.IntegerField()
    number_of_players_in_squad = forms.IntegerField()


class CreateTeamIndividualsForm(forms.ModelForm):
    class Meta:
        model = TeamIndividuals
        fields = ( 'address', 'phone')

    address = forms.CharField(widget=forms.Textarea)
    phone = forms.CharField()


class TeamFormone(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['team_name', 'no_of_players', 'age_category']



class TeamFormtwo(forms.ModelForm):
    class Meta:
        model = Players
        fields = ['player_name']





#TeamFormtwoset = formset_factory(TeamFormtwo, extra=1)

TeamFormtwoset = modelformset_factory(
    Players,
    fields=('player_name', ),
    extra=1,
    widgets={'player_name': forms.TextInput(attrs={
            'class': 'form-control',
        })
    }
)


class TeamFormthree(forms.ModelForm):
    class Meta:
        model = Coaches
        fields = ['coach_name', 'phone_number']

class TeamForfour(forms.ModelForm):
    class Meta:
        model = Team_manager
        fields = ['manager_name', 'phone_number', 'email']



class Coachchangeform(forms.ModelForm):

    class Meta:
        model = Coaches
        fields = ['coach_name', "phone_number"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['coach_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})

def teamregister(request):
    form1 = TeamFormone(request.POST)
    form3 = TeamFormthree(request.POST)
    form4 = TeamForfour(request.POST)
    if request.method == 'GET':
        formset = TeamFormtwoset(queryset=Players.objects.none())
    if request.method == "POST":
        #formset = TeamFormtwo(request.POST)
        formset = TeamFormtwoset(request.POST)
        a_valid = form1.is_valid()
        #b_valid = formset.is_valid()
        c_valid = form3.is_valid()
        d_valid = form4.is_valid()
        # we do this since 'and' short circuits and we want to check to whole page for form errors
        if a_valid and c_valid and d_valid:
            a = form1.save()
            num = request.POST.get('no_of_players')
            for i in range(1,int(num)+1):
                k = "form-"+ str(i) +"-player_name"
                plyobj = Players()
                values_from_user = request.POST.get(k)
                plyobj.player_name = values_from_user
                plyobj.team_id = a
                plyobj.save()
                print('values', values_from_user)
            c = form3.save(commit=False)
            d = form4.save(commit=False)

            c.team_id = a
            c.save()
            d.team_id = a
            d.save()
            messages.success(request, 'Team successfully registered.')
            return redirect('website-home')
    return render(request, 'website/Team_registration.html', {'form1': form1, 'form2': formset, 'form3':form3, 'form4':form4,})

def teamsquad(request):
    team = Team.objects.all()
    return render(request, 'website/Team_squad.html', {'team':team})

def teamdetails(request, team_id):
    team_id = int(team_id)
    tid = Team.objects.get(id = team_id)
    team_data = Players.objects.filter(team_id=team_id)
    coaches_data = Coaches.objects.filter(team_id=team_id)

    if request.method == "POST":
        try:
            num = request.POST.get('no_of_players')
            for i in range(1, int(num) + 1):
                k = "form-" + str(i) + "-player_name"
                plyobj = Players()
                values_from_user = request.POST.get(k)
                plyobj.player_name = values_from_user
                plyobj.team_id = tid
                plyobj.save()
        except:
            pass
    return render(request, 'website/Team_details.html', {'team_data': team_data, 'team_id':team_id, "coaches_data":coaches_data} )

def delete_player(request, pk):
    print(pk)
    Players.objects.filter(id=pk).delete()
    print('check')
    return HttpResponse(content_type="application/json")

# def team_update(request,):
#     return render(request, 'website/Team_update.html')

def coach_update(request, pk):
    # fetch the object related to passed id
    obj = get_object_or_404(Coaches, pk=pk)
    # pass the object as instance in form
    form = Coachchangeform(request.POST or None, instance=obj)
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/team-squad")

    # add form dictionary to context
    context= {'form':form}
    return render(request, "website/update_coach.html", context)


    
