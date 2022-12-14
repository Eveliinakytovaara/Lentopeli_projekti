'use strict'

// const map = L.map("map").setView([51.5074, 0.1278], 5); // London
// L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
//   attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors',
// }).addTo(map);
// const marker1 = L.marker([51.5074, 0.1278]).addTo(map); // London
// const marker2 = L.marker([40.7128, -74.006]).addTo(map); // New York
var map;
var markers = [];
var markerGroup;

var marker1;
var marker2;

//Create map and starting point
function setStartingPoint(startPoint, info) {
    map = L.map("map").setView(startPoint, 5);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors',
    }).addTo(map);
    markerGroup = L.layerGroup().addTo(map);
    setMarker(startPoint, info, "hue-rotate(0deg)");
}

//Create map marker at position
function setMarker(pos, info, rot) {
    let m = L.marker(pos).addTo(markerGroup);
    m._icon.style.filter = rot;
    m.bindPopup(info);
    markers.push(m);
}
//Clear markers created for contries
function clearMarkers() {
    markerGroup.clearLayers();
}
//Zoom to markers
function zoomToMarkers() {
    let group = new L.featureGroup(markers);
    map.fitBounds(group.getBounds());
}

function animateCamera(flight, numSteps, timePerStep) {

    const startPoint = [flight.starting_location.lat, flight.starting_location.lon];
    const endPoint = [flight.ending_location.lat, flight.ending_location.lon];
    
    // Set up the map and the markers
    clearMarkers();
    marker1 = L.marker(startPoint).addTo(map);
    marker1._icon.style.filter = 'hue-rotate(90deg)';

    if (map.hasLayer(marker2)) {
        map.removeLayer(marker2);
    }
    marker2 = L.marker(endPoint).addTo(map);

    // Set up the line
    const line = L.polyline([marker1.getLatLng(), marker2.getLatLng()], {
        color: "red",
    }).addTo(map);

    // Create map and plane html
    let container = document.getElementById('map');
    let paperPlane = document.createElement('div');
    paperPlane.id = 'paper-plane';
    paperPlane.classList.add('paper-plane');
    container.appendChild(paperPlane);

    // Set up the animation
    let step = 0;
    const interval = setInterval(animateCamera, timePerStep);

    function animateCamera() {
        // Calculate the new position of the camera
        const latlng1 = marker1.getLatLng();
        const latlng2 = marker2.getLatLng();
        const lat = latlng1.lat + ((latlng2.lat - latlng1.lat) * step) / numSteps;
        const lng = latlng1.lng + ((latlng2.lng - latlng1.lng) * step) / numSteps;
        const newPosition = L.latLng(lat, lng);

        // Move the camera to the new position
        map.panTo(newPosition);

        // Update the line
        line.setLatLngs([latlng1, newPosition, latlng2]);

        // Calculate the angle of the line at the new position
        const point1 = map.latLngToContainerPoint(latlng1);
        const point2 = map.latLngToContainerPoint(newPosition);
        const angle = (Math.atan2(point2.y - point1.y, point2.x - point1.x) * 180) / Math.PI;

        // Update the position and rotation of the paper plane
        const planePoint = map.latLngToContainerPoint(newPosition);
        paperPlane.style.left = planePoint.x + "px";
        paperPlane.style.top = planePoint.y + "px";
        paperPlane.style.transform = "rotate(" + angle + "deg)";
        L.imagaOverlay

        // Increment the step
        step++;

        // Stop the animation if we've reached the end
        if (step >= numSteps) {
            clearInterval(interval);
            paperPlane.remove();
            map.removeLayer(marker1);
            finnishFlight(flight);
        }
    }
}


function animateFlying(flight) {
    // example: animateCamera([51.5074, 0.1278], [40.7128, -74.006], map, 1000, 10);    
    animateCamera(flight, 250, 5);
}
