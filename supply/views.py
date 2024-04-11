
from django.shortcuts import render
import googlemaps
from django.conf import settings
import openai
import pathlib
import textwrap
import google.generativeai as genai
from django.core.files.storage import FileSystemStorage
import os
import PIL.Image
from django.http import JsonResponse



x = []

def to_markdown(text):
  text = text.replace('•', '  *')
  return textwrap.indent(text, '', predicate=lambda _: True)

def supply(request):

    global x
    GOOGLE_API_KEY='AIzaSyDtiq-CBPFG500PMG_UJtO08wf4EQnz9H4'
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    if request.method == 'GET':
        initial_message = 'Hello! How can I assist you?'
        return render(request, 'supply.html', {'initial_message': initial_message})
    
    elif request.method == 'POST':
        prompt = request.POST.get('message', '')
        user_message = f"""
                        -limit your responce within 50 words for the following prompt
                        - prompt =  {prompt}
                        """
        response = model.generate_content(user_message)
        result = to_markdown(response.text)
        chatbot_response = result
        return JsonResponse({'message': chatbot_response})
    else:
        return JsonResponse({'error': 'Invalid request method'})




    # if request.method == 'POST':
    #     api_key = settings.GOOGLE_MAPS_API_KEY

    #     source_lat = request.POST.get('source_lat')
    #     source_lng = request.POST.get('source_lng')
    #     dest_lat = request.POST.get('dest_lat')
    #     dest_lng = request.POST.get('dest_lng')

    #     gmaps = googlemaps.Client(key=api_key)

    #     # Construct the directions request
    #     directions = gmaps.directions(
    #         f'{source_lat},{source_lng}',
    #         f'{dest_lat},{dest_lng}',
    #         mode='driving'  # Specify the mode of travel, such as driving, walking, etc.
    #     )

    #     if directions:
    #         # Construct the navigation URL from the directions response
    #         navigation_url = f'https://www.google.com/maps/embed/v1/directions?key={api_key}&origin={source_lat},{source_lng}&destination={dest_lat},{dest_lng}'

    #         return render(request, 'supply.html', {'navigation_url': navigation_url})
    # return render(request, 'supply.html', {'result': result})

