var map = L.map('map').setView([{{ lat }}, {{ lon }}], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: 'Map data copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
}).addTo(map);

{% for location in locations %}
var marker = L.marker([{{ location.lat }}, {{ location.lon }}]).addTo(map);
marker.bindPopup("<b>{{ location.name }}</b><br>{{ location.description }}");
{% endfor %}

var pathPoints = [
    {% for location in locations %}
    [{{ location.lat }}, {{ location.lon }}],
    {% endfor %}
];

var path = L.polyline(pathPoints, {color: 'red'}).addTo(map);

var carIcon = L.icon({
    iconUrl: 'https://cdn4.iconfinder.com/data/icons/car-silhouettes/1000/car-6-128.png',
    iconSize: [32, 32],
    iconAnchor: [16, 16]
});

var movingMarker = L.Marker.movingMarker(pathPoints, [5000]).setIcon(carIcon).addTo(map);
movingMarker.start();
