'use strict'

// const map = L.map("map").setView([51.5074, 0.1278], 5); // London
// L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
//   attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors',
// }).addTo(map);
// const marker1 = L.marker([51.5074, 0.1278]).addTo(map); // London
// const marker2 = L.marker([40.7128, -74.006]).addTo(map); // New York

function animateCamera(startPoint, endPoint, map, numSteps, timePerStep) {
    // Set up the map and the markers

    const marker1 = L.marker(startPoint).addTo(map);
    const marker2 = L.marker(endPoint).addTo(map);

    // Set up the line
    const line = L.polyline([marker1.getLatLng(), marker2.getLatLng()], {
        color: "red",
    }).addTo(map);

    // Set up the animation
    let step = 0;
    const interval = setInterval(animateCamera, timePerStep);

    // Set up the paper plane
    const paperPlane = document.getElementById("paper-plane");
    

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

        // Increment the step
        step++;

        // Stop the animation if we've reached the end
        if (step >= numSteps) {
            clearInterval(interval);
        }
    }
}


function animateFlying(startPoint, endPoint) {
    const map = L.map("map").setView([51.5074, 0.1278], 5); // London
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors',
    }).addTo(map);

    // example: animateCamera([51.5074, 0.1278], [40.7128, -74.006], map, 1000, 10);    
    animateCamera(startPoint, endPoint, map, 1000, 10);
}


