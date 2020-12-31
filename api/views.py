from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework import mixins
from rest_framework import generics
from .models import Preference, Politician, Profile, Event, calculatePoliticalScore, Movement
from .serializers import PreferenceSerializers, PoliticianSerializers, ProfileSerializers
from rest_framework.authtoken.models import Token


# importing googlemaps module 
import googlemaps 

# Defining API key variable
gmaps = googlemaps.Client(key='AIzaSyCp6FcON1WLE_CnVGL4_jT8j5sUqK97wss')


# Creating view for people to request to add change or delete politicians
def changeProfileData(request):
    
    return render(request, 'homepage/change_politician_profile.html')
    
class GetPoliticianInfo(generics.RetrieveAPIView,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):

    def list(self, request, pk=None):

        # Creating variable that will be returned
        returnDict = dict()
        
        # Creating token variable
        token = None
        try:
            # Getting token
            token = str(request.META['HTTP_AUTHORIZATION'])[6:]
            print(token)

            # Getting User
            token = Token.objects.get(key=token)

            user = token.user

            # Getting profile and user location
            profile = Profile.objects.get(user=user)
            userLocation = profile.location
        except Exception as e:
            print(e)

        
        # Defining the defaults for start attribute and number attribute

        # Number is the number of people will be returned
        number = 5
        try:
            number = int(request.META['HTTP_NUMBER'])
        except Exception as e:
            print(e)

        # Start is the id of the object in which we get objects
        start = 1
        try:
            start = int(request.META['HTTP_START'])
        except Exception as e:
            print(e)
        
        print(request.META)
        print('Number: ', number)
        print('Start: ', start)
        

        # Trying to get nearby variable to see if we are returning nearby politicians or not
        nearby = False
        try:
            # Getting posted location
            userLocation = request.META['HTTP_LOCATION']
            nearby = True
        except Exception as e:
            print(e)

        # Creating list of politician data
        politicians = []
        
        # Getting list of politicians will filter to limit the amount of data in request
        start -= 1
        counter = 0
        for item in Politician.objects.all():
            # do something with item
            # print("item")
            # print(item.pk)
            politicianId = item.pk + start
            try:
                politicians.append(Politician.objects.filter(pk=politicianId).values()[0])
            except Exception as e:
                print(e)
                print("e")
            
            counter += 1
            if counter == number:
                break

        # politicians = Politician.objects.all().values()
        # politicians = list(politicians)
        print("politicians")
        # print(politicians)

        # Checking if token exist
        if token is None or token == 'null':
            print('sdsd')
            for x in politicians:
                # Getting specific politician preferences
                # print(x['preference_id'])
                preferences = Preference.objects.filter(pk=x['preference_id']).values()
                preferences = list(preferences)
                preferences = preferences[0]
                x['preferences'] = preferences
                
                x['image'] = Politician.objects.get(pk=x['id']).image.url

                # Deleting id of preference
                del x['preference_id']
                del x['preferences']['id']

                # Getting and saving overall political score
                score = calculatePoliticalScore(preferences['social_left_to_right'], preferences['economics_left_to_right'])
                x['score'] = score

                x['similar_views'] = []

            returnDict['politicians'] = politicians
        else:
            print('great!')
            
            # Getting user preferences to later compare with other politician views
            username = user.username
            userPreference = Preference.objects.filter(owner=username).values()[0]

            # Looping through politicians
            for x in politicians:
                
                # Getting preferences
                preferences = Preference.objects.filter(owner=x['name']).values()[0]

                # Getting image
                x['image'] = Politician.objects.get(pk=x['id']).image.url

                # Getting location
                politicianLocation = x['location']

                # Creating list of similar views
                similarViews = []

                # Looping through and comparing preferences
                for preference in preferences:
                    # print("preference")
                    # print(preference)
                    # print(preferences[preference])

                    # Checking if preference is simalar
                    if preferences[preference] == userPreference[preference]:
                        # print(preference)
                        similarViews.append(preference)
                x['similar_views'] = similarViews

                # Defaulting distance of politician to an impossible number, 45,000,000
                x['distance'] = 45000000

                # Checking if nearby is true and if so getting distance from user using google maps api
                if nearby == True:
                    print('nearby')

                    # Making request and getting distance in meters
                    if politicianLocation:

                        # Getting status 
                        distanceRequest = gmaps.distance_matrix(politicianLocation, userLocation)['rows'][0]['elements'][0]

                        # Checking if request was ok
                        if distanceRequest['status'] == 'OK':

                            # Getting distance between user and politician in meters
                            meters = distanceRequest['distance']['value']

                            # Adding to dict
                            x['distance'] = meters

            politicians = sorted(politicians, key=lambda k: k['distance']) 

            returnDict['politicians'] = politicians

        # Returning and OK status
        returnDict['status'] = 'OK'

        return Response(returnDict)

class GetEventInfo(generics.RetrieveAPIView,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):

    def list(self, request, pk=None):

        # Creating variable that will be returned
        returnDict = dict()
        
        # Creating token variable
        token = None
        try:
            # Getting token
            token = str(request.META['HTTP_AUTHORIZATION'])[6:]
            print(token)

            # Getting User
            token = Token.objects.get(key=token)

            user = token.user
            
            # Getting location
            profile = Profile.objects.get(user=user)
            userLocation = profile.location

        except Exception as e:
            print(e)
        

        # Defining the defaults for start attribute and number attribute

        # Number is the number of people will be returned
        number = 5
        try:
            number = int(request.META['HTTP_NUMBER'])
        except Exception as e:
            print(e)

        # Start is the id of the object in which we get objects
        start = 1
        try:
            start = int(request.META['HTTP_START'])
        except Exception as e:
            print(e)
        
        print(request.META)
        print('Number: ', number)
        print('Start: ', start)

        # Trying to get nearby variable to see if we are returning nearby politicians or not
        nearby = False
        try:
            # Getting posted location
            userLocation = request.META['HTTP_LOCATION']
            nearby = True
        except Exception as e:
            print(e)

        # Creating list of events data
        events = []
        
        start -= 1
        counter = 0
        for item in Event.objects.all():
            # do something with item
            # print("item")
            # print(item.pk)
            eventId = item.pk + start
            try:
                events.append(Event.objects.filter(pk=eventId).values()[0])
            except Exception as e:
                print(e)
                print("e")
            
            counter += 1
            if counter == number:
                break

        print("events")
        print(events)

        # Checking if token exist
        if token is None or token == 'null':
            print('sdsd')
            for x in events:
                
                # Adding image to the event object
                x['image'] = Event.objects.get(pk=x['id']).image.url

            returnDict['events'] = events
        else:
            print('great!')
            
            # Creating list that will store dictionaries of ids and distance from user
            eventDistance = []

            # Looping through events
            for x in events:
                
                # Getting image
                x['image'] = Event.objects.get(pk=x['id']).image.url

                # Getting location
                eventAddress = x['address']
                eventCity = x['city']
                eventLocation = x['address'] + " " + x['city']


                # Defaulting distance of politician to an impossible number, 45,000,000
                x['distance'] = 45000000

                # Checking if nearby is true and if so getting distance from user using google maps api
                if nearby == True:
                    # print('nearby')

                    # Making request and getting distance in meters
                    if eventLocation:

                        # Getting status 
                        distanceRequest = gmaps.distance_matrix(eventLocation, userLocation)['rows'][0]['elements'][0]

                        # Checking if request was ok
                        if distanceRequest['status'] == 'OK':

                            # Getting distance between user and politician in meters
                            meters = distanceRequest['distance']['value']

                            # Adding to dict
                            x['distance'] = meters

            events = sorted(events, key=lambda k: k['distance']) 

            returnDict['events'] = events
        returnDict['status'] = 'OK'

        return Response(returnDict)
        

class GetMovementInfo(generics.RetrieveAPIView,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):

    def list(self, request, pk=None):

        # Creating variable that will be returned
        returnDict = dict()
        
        # Creating token variable
        token = None
        try:
            # Getting token
            token = str(request.META['HTTP_AUTHORIZATION'])[6:]
            print(token)

            # Getting User
            token = Token.objects.get(key=token)

            user = token.user
            
            # Getting location
            profile = Profile.objects.get(user=user)
            userLocation = profile.location

        except Exception as e:
            print(e)
        

        # Defining the defaults for start attribute and number attribute

        # Number is the number of people will be returned
        number = 5
        try:
            number = int(request.META['HTTP_NUMBER'])
        except Exception as e:
            print(e)

        # Start is the id of the object in which we get objects
        start = 1
        try:
            start = int(request.META['HTTP_START'])
        except Exception as e:
            print(e)
        
        print(request.META)
        print('Number: ', number)
        print('Start: ', start)


        # Creating list of movement data
        movements = []
        
        start -= 1
        counter = 0
        for item in Movement.objects.all():
            # do something with item
            # print("item")
            # print(item.pk)
            movementId = item.pk + start
            try:
                movements.append(Movement.objects.filter(pk=movementId).values()[0])
            except Exception as e:
                print(e)
                print("e")
            
            counter += 1
            if counter == number:
                break

        print("events")
        print(movements)

        returnDict['movements'] = movements
        returnDict['status'] = 'OK'

        return Response(returnDict)
        

        