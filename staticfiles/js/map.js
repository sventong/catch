let map;

async function initMap() {
    const { Map } = await google.maps.importLibrary("maps");
    
    map = new Map(document.getElementById("map"), {
        center: { lat: 48.137154, lng: 11.576124 },
        zoom: 8,
    });
    map.setMyLocationEnabled(true);


    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const pos = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude,
                };

                // infoWindow.setPosition(pos);
                // infoWindow.setContent("Location found.");
                // infoWindow.open(map);
                map.setCenter(pos);
            },
            () => {
                handleLocationError(true, infoWindow, map.getCenter());
            }
        );
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, infoWindow, map.getCenter());
    };
}





function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(
    browserHasGeolocation
        ? "Error: The Geolocation service failed."
        : "Error: Your browser doesn't support geolocation."
    );
    infoWindow.open(map);
}


initMap();




// const copy = "&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors";
// const url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
// const layer = L.tileLayer(url, { attribution: copy });


// function onLocationFound(e) {
//     var radius = e.accuracy / 2;
//     L.marker(e.latlng).addTo(map)
//       .bindPopup("You are within " + radius + " meters from this point").openPopup();
//     L.circle(e.latlng, radius).addTo(map);
// }


// const map = L.map("map", { layers: [layer] })
// map.on('locationfound', onLocationFound);
// map.locate({setView: true, watch: true, maxZoom: 16});

// map.fitWorld();