

const copy = "&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors";
const url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
const layer = L.tileLayer(url, { attribution: copy });


function onLocationFound(e) {
    var radius = e.accuracy / 2;
    L.marker(e.latlng).addTo(map)
      .bindPopup("You are within " + radius + " meters from this point").openPopup();
    L.circle(e.latlng, radius).addTo(map);
}


const map = L.map("map", { layers: [layer] })
map.on('locationfound', onLocationFound);
map.locate({setView: true, watch: true, maxZoom: 16});

map.fitWorld();