import requests
import folium
from folium.plugins import AntPath
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Define the location of Mahabaleshwar, Maharashtra, India
    location = 'Mahabaleshwar, Maharashtra, India'

    # Define the URL for the OpenStreetMap API
    url = f'https://nominatim.openstreetmap.org/search?q={location}&format=json'

    # Send a GET request to the API
    response = requests.get(url)

    # Get the latitude and longitude of the location
    latitude = float(response.json()[0]['lat'])
    longitude = float(response.json()[0]['lon'])

    # Define the URL for the Overpass API to search for tourist attractions
    overpass_url = 'https://overpass-api.de/api/interpreter'

    # Define the Overpass query to search for tourist attractions in Mahabaleshwar
    overpass_query = f"""
        [out:json];
        (
          node["tourism"="attraction"]({latitude - 0.1},{longitude - 0.1},{latitude + 0.1},{longitude + 0.1});
          way["tourism"="attraction"]({latitude - 0.1},{longitude - 0.1},{latitude + 0.1},{longitude + 0.1});
          relation["tourism"="attraction"]({latitude - 0.1},{longitude - 0.1},{latitude + 0.1},{longitude + 0.1});
        );
        out center;
        """

    # Send a POST request to the Overpass API with the query
    response = requests.post(overpass_url, data=overpass_query)

    # Get the JSON response and extract the tourist attractions
    data = response.json()
    attractions = [x['tags']['name:en'] for x in data['elements']]

    # Create a folium map centered on Mahabaleshwar
    m = folium.Map(location=[latitude, longitude], zoom_start=13)

    # Add a marker for Mahabaleshwar
    folium.Marker([latitude, longitude], popup='Mahabaleshwar', icon=folium.Icon(color='green')).add_to(m)

    # Add markers for the tourist attractions
    marker_list = []
    for element in data['elements']:
        popup_text = element['tags']['name:en'] if 'name:en' in element['tags'] else 'Unnamed Place'
        marker = folium.Marker([element['lat'], element['lon']], popup=popup_text, tooltip=popup_text, icon=folium.Icon(color='red'))
        marker.add_to(m)
        marker_list.append(marker)

    # Draw a path connecting all the markers for the tourist attractions
    locations = [[marker.location[0], marker.location[1]] for marker in marker_list]
    path = AntPath(locations=locations, color='blue', dash_array=[10, 20], delay=800)
    path.add_to(m)
    # m.save("./Pune_Bus_Stops.html")

    # Render the map in an HTML template using Flask's render_template function
    return render_template('index.html', map=m._repr_html_())

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9000, debug=True)
