from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from . import views



class TestClass(TestCase):
    request = []
    
    def individualRegistrationTest(self):
        responseType =  "<class 'django.http.response.HttpResponse'>"
        response = views.getRefreePage(self.request)
        self.assertEquals(str(response.__class__), responseType, msg='Equal')
    
    def homeTest(self):
        responseType =  "<class 'django.template.response.TemplateResponse'>"
        response = views.home(self.request)
        self.assertEquals(str(response.__class__), responseType, msg='Equal')
    
    def getVolunteerPageTest(self):
        responseType =  "<class 'django.http.response.HttpResponse'>"
        response = views.getVolunteerPage(self.request)
        self.assertEquals(str(response.__class__), responseType, msg='Equal')
    
    def matchScheduleTest(self):
        responseType =  "<class 'django.http.response.HttpResponse'>"
        response = views.getVolunteerPage(self.request)
        self.assertEquals(str(response.__class__), responseType, msg='Equal')
    
    def addTeamTest(self):
        responseType =  "<class 'django.http.response.HttpResponse'>"
        response = views.getVolunteerPage(self.request)
        self.assertEquals(str(response.__class__), responseType, msg='Equal')
    
    def matchReportTest(self):
        responseType =  "<class 'django.http.response.HttpResponse'>"
        response = views.getVolunteerPage(self.request)
        self.assertEquals(str(response.__class__), responseType, msg='Equal')
    
    def getMapPageTest(self):
        responseType =  "<class 'django.http.response.HttpResponse'>"
        response = views.getVolunteerPage(self.request)
        self.assertEquals(str(response.__class__), responseType, msg='Equal')

    def getRefreePageTest(self):
        responseType =  "<class 'django.http.response.HttpResponse'>"
        response = views.getVolunteerPage(self.request)
        self.assertEquals(str(response.__class__), responseType, msg='Equal')
    
    def getLiveTournamentsTest(self):
        responseType =  "<class 'django.http.response.HttpResponse'>"
        response = views.getVolunteerPage(self.request)
        self.assertEquals(str(response.__class__), responseType, msg='Equal')
    
    def getInventoryTest(self):
        responseType =  "<class 'django.http.response.HttpResponse'>"
        response = views.getVolunteerPage(self.request)
        self.assertEquals(str(response.__class__), responseType, msg='Equal')   

    

    

t = TestClass()
t.individualRegistrationTest()
t.homeTest()
t.getVolunteerPageTest()
t.matchScheduleTest()
t.matchScheduleTest()
t.addTeamTest()
t.matchReportTest()
t.getMapPageTest()
t.getRefreePageTest()
t.getLiveTournamentsTest()
t.getInventoryTest()
# Create your tests here.
