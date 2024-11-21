// Initialise map
let map = L.map('map', {maxZoom: 19, minZoom:15, maxBounds: [[52.13, 4.455],[52.19, 4.53]], zoom: 17, center: [52.1581218,4.4855674]});

// // Google streets map
// let googleStreets = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',{
// maxZoom: 20,
// subdomains:['mt0','mt1','mt2','mt3']
// });
// googleStreets.addTo(map);

// Show map layer
let mapLayer = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
// maxBoundsViscosity: 1.0
}).addTo(map);  
// map.fitBounds([[52,4.3],[52.2,4.6]])

// Add start and end positions and put their markers
let startPos = [52.1581218,4.4855674],
endPos = [52.162853,4.4826858];
startMarker = L.marker(startPos).addTo(map).bindPopup("Rijksmuseum van Oudheden");
endMarker = L.marker(endPos).addTo(map).bindPopup("Wereldmeseum Leiden");

//Create circleIcon
let circleIcon = L.icon({
iconUrl: 'circle_icon.png',
iconSize: [16, 16],
iconAnchor: [8, 8],
popupAnchor: [8, 8]
});

//Create path
console.log(startMarker);
let path = [startMarker.getLatLng()],
polyline = L.polyline(path, {color: '#7e7e7e'}).addTo(map),
//repeaterLines stores the polylines for all the edges that have been crossed twice
// repeatedEdges = []

// Temporarily add arbitrary positions
markers = [],
coordinates = [[52.16,4.49], [52.159,4.491], [52.16,4.492]];

// blockedRoads is the list of all roads that can't be traversed due to being blocked
let blockedRoads = [[[52.159,4.491],[52.16,4.492]]];
blockedRoads.forEach(function(blockedRoad) {
    L.polyline(blockedRoad, {color: '#dd0000'}).addTo(map);
});

// Make markers with these positions, with an event that makes it so that you can add them to the path
// by clicking on then
coordinates.forEach(function(coords) {
    let marker = L.marker(coords, {icon: circleIcon}).addTo(map).bindPopup();
    marker.on('click', function(e) {
        console.log(path);
        console.log(e.latlng)
        path.forEach(function(node) {
            console.log("node: " + node)
            if (e.latlng.equals(node)) {
                L.polyline([e.latlng, path.at(-1)], {color: '#343434'}).addTo(map);
                // console.log(repeatedEdges);
            }
        });
        // if (e.latlng in path) {
        //     repeatedEdges.push(L.polyline([e.latlng, path[-1]], {color: '#343434'}).addTo(map));
        //     console.log(repeatedEdges);
        // }
        path.push(e.latlng);
        polyline.setLatLngs(path);
        marker.closePopup();
        // score++;
    });
    markers.push(marker);
});


// let adjNodeGroup = L.featureGroup(markers).addTo(map).bindPopup("");
