import requests
import folium
from folium.plugins import AntPath
from flask import Flask, render_template
import math

app = Flask(__name__)

bus_stops = [
            {"Katraj": {"lat": 18.446981,  "long": 73.858604}},
            {"Swarget": {"lat": 18.499869,  "long": 73.858242}},
            {"Deccan": {"lat": 18.516287,  "long": 73.842758}},
            # {"Shivaji Nagar": {"lat": 18.531597,  "long": 73.849592}},
            # {"Kothrud": {"lat": 18.507247,  "long": 73.807519}},
            # {"Fatima Nagar": {"lat": 18.505240,  "long": 73.900989}},
            # {"Magarpatta": {"lat": 18.514112,  "long": 73.932414}},
            # {"Koregao Park": {"lat": 18.535516,  "long": 73.911891}},
            # {"Viman Nagar": {"lat": 18.565107,  "long": 73.911274}},
            # {"Khadki": {"lat": 18.561463, "long": 73.852817}}
        ]

pune = folium.Map(location=[18.520804, 73.855337], zoom_start=13)
live_sites = ["Katraj", "Swarget", "Kothrud", "Khadki", "Magarpatta", "Koregao Park"]
current_position = None


#
# def plot_bus_stop_locations():
#     for bus_stop in bus_stops:
#         for name, location in bus_stop.items():
#             if name in live_sites:
#                 folium.Marker(location=[location["lat"], location["long"]], popup=name,
#                               icon=folium.Icon(color='green')).add_to(pune)
#             else:
#                 folium.Marker(location=[location["lat"], location["long"]], popup=name,
#                               icon=folium.Icon(color='red')).add_to(pune)
#
#
# def plot_current_location():
#     # current_position = {"lat": 18.545822, "long": 73.912112}
#     current_position = {"lat": 18.512024, "long": 73.831562}
#     folium.Marker(location=[current_position["lat"], current_position["long"]], popup="current location",
#                   icon=folium.Icon(color='blue', prefix='fa', icon='car')).add_to(pune)
#
#
def degrees_to_radians(degrees):
    return degrees * math.pi / 180
#
#
def distance_in_km_between_two_coordinates(lat1, lon1, lat2, lon2):
    earthRadiusKm = 6378.14

    dLat = degrees_to_radians(lat2 - lat1)
    dLon = degrees_to_radians(lon2 - lon1)

    lat1 = degrees_to_radians(lat1)
    lat2 = degrees_to_radians(lat2)

    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.sin(dLon / 2) * math.sin(dLon / 2) * math.cos(lat1) * math.cos(
        lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(earthRadiusKm * c, 2)
#
#
# def calculate_distance_from_current_location_to_bus_stop():
#     distance_list = []
#     for bus_stop in bus_stops:
#         for name, location in bus_stop.items():
#             if name not in live_sites:
#                 distance = distance_in_km_between_two_coordinates(current_position["lat"],
#                                                                        current_position["long"], location["lat"],
#                                                                        location["long"])
#                 distance_list.append({"bus_stop": name, "distance": distance})
#     return distance_list
#
#
# def print_distance(distance_list):
#     for info in distance_list:
#         print("Distance from your current location to", info["bus_stop"], "is", info["distance"])
#
#
# def near_location(distance_list):
#     distance_list.sort(key=lambda x: x["distance"])
#     for data in distance_list:
#         print(f"You are near {data['bus_stop']}. Distance is {data['distance']} KM")
#         return
#
#
# def stops_near_to_you_within_3kms(distance_list):
#     distance_list.sort(key=lambda x: x["distance"])
#     for data in distance_list:
#         if data["distance"] <= 3:
#             print(f"You are near {data['bus_stop']}. Distance is {data['distance']} KM")
#             return

@app.route('/')
def main():
    for bus_stop in bus_stops:
        for name, location in bus_stop.items():
            if name in live_sites:
                folium.Marker(location=[location["lat"], location["long"]], popup=name,
                              icon=folium.Icon(color='green')).add_to(pune)
            else:
                folium.Marker(location=[location["lat"], location["long"]], popup=name,
                              icon=folium.Icon(color='red')).add_to(pune)


    # plot_bus_stop_locations()
    # plot_current_location()
    current_position = {"lat": 18.512024, "long": 73.831562}
    folium.Marker(location=[current_position["lat"], current_position["long"]], popup="current location",
                  icon=folium.Icon(color='blue', prefix='fa', icon='car')).add_to(pune)
    # distance_list = calculate_distance_from_current_location_to_bus_stop()
    # distance_list = []
    # for bus_stop in bus_stops:
    #     for name, location in bus_stop.items():
    #         if name not in live_sites:
    #             distance = distance_in_km_between_two_coordinates(current_position["lat"],
    #                                                               current_position["long"], location["lat"],
    #                                                               location["long"])
    #             distance_list.append({"bus_stop": name, "distance": distance})
    # # print_distance(distance_list)
    # for info in distance_list:
    #     print("Distance from your current location to", info["bus_stop"], "is", info["distance"])
    # print()
    # # near_location(distance_list)
    # distance_list.sort(key=lambda x: x["distance"])
    # for data in distance_list:
    #     print(f"You are near {data['bus_stop']}. Distance is {data['distance']} KM")
    #     return
    # print()
    # # stops_near_to_you_within_3kms(distance_list)
    # distance_list.sort(key=lambda x: x["distance"])
    # for data in distance_list:
    #     if data["distance"] <= 3:
    #         print(f"You are near {data['bus_stop']}. Distance is {data['distance']} KM")
    #         # break
    #         return
    pune.save('templates/map.html')

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
