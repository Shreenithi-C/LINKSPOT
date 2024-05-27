
from django.shortcuts import render
import googlemaps
from django.conf import settings
#import openai
import pathlib
import textwrap
import google.generativeai as genai
from django.core.files.storage import FileSystemStorage
import os
import PIL.Image
from django.http import JsonResponse
from .models import Hotspot,Restaurant
import json
from .models import FoodRequest
import uuid


def home(request):
    return render(request, 'home.html')

x = []

def to_markdown(text):
  text = text.replace('•', '  *')
  return textwrap.indent(text, '', predicate=lambda _: True)

def supply(request):

    rest_name = []
    food_avail = []

    api_key = settings.GOOGLE_MAPS_API_KEY
    gmaps = googlemaps.Client(key=api_key)

    restaurants = Restaurant.objects.values('Restaurant_Name','Food_available').order_by('-Food_available')

    for i in restaurants:
        rest_name.append(i['Restaurant_Name'])
        food_avail.append(i['Food_available'])
    
    rest_name = rest_name[:5]
    food_avail = food_avail[:5]


    Hotspot_name =[]
    Food_needed = []

    hotspots = Hotspot.objects.values('Hotspot_Name','Food_needed').order_by('-Food_needed')

    for i in hotspots:
        Hotspot_name.append(i['Hotspot_Name'])
        Food_needed.append(i['Food_needed'])
    
    Hotspot_name = Hotspot_name[:5]
    Food_needed = Food_needed[:5]

    latitudes = list(Hotspot.objects.values_list('Hotspot_Latitude', flat=True))
    longitudes = list(Hotspot.objects.values_list('Hotspot_longitude', flat=True))
    coordinates = list(zip(latitudes, longitudes))

    print(Hotspot_name)
    global x
    GOOGLE_API_KEY='AIzaSyDtiq-CBPFG500PMG_UJtO08wf4EQnz9H4'
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    global a,b,c,d
    # source = request.GET.get('source')
    # x=source
    # rest = Hotspot.objects.get(Hotspot_Name = x)
    # urge = rest.Food_needed
    # to_ai_scarce = {x:urge}
    # print(to_ai_scarce)
    # source_lat = float(rest.Hotspot_Latitude)
    # source_long = float(rest.Hotspot_longitude)


    # origin = f"{source_lat},{source_long}"

    # choice_rest = Restaurant.objects.values('Restaurant_Name','Restaurant_Latitude','Restaurant_longitude','Food_available')

    # choice_dict = {}

    # for i in choice_rest:
    #     dest_name = i['Restaurant_Name'] + " - " + str(i['Food_available']) + " KGs"
    #     dest_lat = float(i['Restaurant_Latitude'])
    #     dest_long = float(i['Restaurant_longitude'])
    #     destination = f"{dest_lat},{dest_long}"

    #     directions = gmaps.directions(origin, destination, mode="driving")
    #     distance_in_meters = directions[0]['legs'][0]['distance']['value']
    #     distance_in_km = distance_in_meters / 1000

    #     choice_dict[dest_name] = distance_in_km
    
    # choice_dict = dict(sorted(choice_dict.items(), key=lambda item: item[1]))

    # choice_dict = dict(list(choice_dict.items())[:4])

    # print(choice_dict)


    if request.method == 'GET':
        initial_message = 'Hello! How can I assist you?'

        source = request.GET.get('source')
        print('the source is :',source)
        if source is None:
            a = 'Gandhipuram'
        else:
            a=source
        rest = Hotspot.objects.get(Hotspot_Name = a)
        urge = rest.Food_needed
        b = {a:urge}
        print(b)
        source_lat = float(rest.Hotspot_Latitude)
        source_long = float(rest.Hotspot_longitude)


        origin = f"{source_lat},{source_long}"

        choice_rest = Restaurant.objects.values('Restaurant_ID','Restaurant_Name','Restaurant_Latitude','Restaurant_longitude','Food_available')

        choice_dict = {}

        for i in choice_rest:
            dest_name = 'ID : ' + str(i['Restaurant_ID']) + ' - ' + i['Restaurant_Name'] + " - " + str(i['Food_available']) + " KGs"
            dest_lat = float(i['Restaurant_Latitude'])
            dest_long = float(i['Restaurant_longitude'])
            destination = f"{dest_lat},{dest_long}"

            directions = gmaps.directions(origin, destination, mode="driving")
            distance_in_meters = directions[0]['legs'][0]['distance']['value']
            distance_in_km = distance_in_meters / 1000

            choice_dict[dest_name] = distance_in_km
        
        choice_dict = dict(sorted(choice_dict.items(), key=lambda item: item[1]))

        choice_dict = dict(list(choice_dict.items())[:4])

        c = choice_dict

        print(choice_dict)
        return render(request, 'supply.html', {'initial_message': initial_message,'hotspot':hotspots,'Hotspot_Name':Hotspot_name,'Food_needed':Food_needed, 'coordinates':json.dumps(coordinates),'api':api_key,'rest_name':rest_name,'food_avail':food_avail,'res':choice_dict})
    
    elif request.method == 'POST':
        prompt = request.POST.get('message', '')
        user_message = f"""
                        - You need to act as a optimization engineer and provide results for quicker solving of hunger in scarce areas.
                        - Provide a proper reasoning. Never provide python code.
                        - Your response should be within 50 words. Not more than that.
                        - You are given with two dictionaries.
                        - The first dictionary consist of an area name where there is food scarcity and the amount of food needed in that area.
                        - The second dictionary consist of the nearby hotels with hotel name, food available in the hotel and the distance between the scarce area and the hotel.
                        - Your task is to analyse both the dictionaries and provide the best restaurant that needs to be approached so that the scarcity can be resolved quickly.
                        - Dont get to the conclusion, 'if the distance is less then that is the answer'. Do consider all the hotels based on both distance and food available to serve.
                        - Consider both food available and also the distance as constraints.
                        - food scarce dictionary = {b}
                        - Nearby restaurant dictionary = {c}
                        - User prompt = {prompt}

                        
                        """
        response = model.generate_content(user_message)
        result = to_markdown(response.text)
        chatbot_response = result
        return JsonResponse({'message': chatbot_response})
    else:
        return JsonResponse({'error': 'Invalid request method'})


identifier = ''
def user_page(request):
    global identifier
    if request.method == 'POST':
        rest_id = request.POST.get('restaurant_id')
        user_name = request.POST.get('user_name')
        food_details = request.POST.get('food_details')
        # Generate a unique user identifier (UUID)
        user_identifier = str(uuid.uuid4())
        identifier = user_identifier
        FoodRequest.objects.create(Restaurant_ID = rest_id ,Supplier_name=user_name, food_details=food_details, user_identifier=user_identifier)
        return JsonResponse({'status': 'success', 'user_identifier': user_identifier})
    requests = FoodRequest.objects.all()[::-1][:5]
    
    return render(request, 'user_page.html',{'requests':requests})

def restaurant_page(request):
    requests = FoodRequest.objects.filter(status='Pending')
    details = FoodRequest.objects.all()[::-1][:5]
    return render(request, 'restaurant_page.html', {'requests': requests,'details':details})

def accept_request(request, request_id):
    food_request = FoodRequest.objects.get(pk=request_id)
    food_request.status = 'Accepted'
    food_request.save()
    return JsonResponse({'status': 'success'})

def reject_request(request, request_id):
    food_request = FoodRequest.objects.get(pk=request_id)
    food_request.status = 'Rejected'
    food_request.save()
    return JsonResponse({'status': 'success'})

def check_notification(request):
    global identifier
    user_identifier = request.GET.get('user_identifier')  # Get the user identifier from the request
    if user_identifier:
        # Check if there are any accepted requests for the user identifier
        if FoodRequest.objects.filter(user_identifier=identifier, status='Accepted').exists():
            message = 'Your request has been accepted!'
        else:
            message = 'No request'

    return JsonResponse({'message': message})

def navigate(request):
    accepted_requests = FoodRequest.objects.filter(status = 'Accepted')[::-1]
    ID = accepted_requests[0].Restaurant_ID

    to_restaurant = Restaurant.objects.filter(Restaurant_ID = int(ID))

    to_lat = to_restaurant[0].Restaurant_Latitude
    to_long = to_restaurant[0].Restaurant_longitude

    api_key = settings.GOOGLE_MAPS_API_KEY

    return render(request, 'navigate.html',{'latitude':to_lat,'longitude':to_long,'api':api_key})

