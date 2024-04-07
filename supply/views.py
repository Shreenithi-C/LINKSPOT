
from django.shortcuts import render
import googlemaps
from django.conf import settings

def navigate(request):
    if request.method == 'POST':
        api_key = settings.GOOGLE_MAPS_API_KEY

        source_lat = request.POST.get('source_lat')
        source_lng = request.POST.get('source_lng')
        dest_lat = request.POST.get('dest_lat')
        dest_lng = request.POST.get('dest_lng')

        gmaps = googlemaps.Client(key=api_key)

        # Construct the directions request
        directions = gmaps.directions(
            f'{source_lat},{source_lng}',
            f'{dest_lat},{dest_lng}',
            mode='driving'  # Specify the mode of travel, such as driving, walking, etc.
        )

        if directions:
            # Construct the navigation URL from the directions response
            navigation_url = f'https://www.google.com/maps/embed/v1/directions?key={api_key}&origin={source_lat},{source_lng}&destination={dest_lat},{dest_lng}'

            return render(request, 'navigation.html', {'navigation_url': navigation_url})
        else:
            return render(request, 'error.html', {'message': 'Error fetching directions'})

    return render(request, 'navigation_form.html')

