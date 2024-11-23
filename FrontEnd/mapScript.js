// // Add start and end positions and put their markers
// let startPos = [52.1581218,4.4855674],
// endPos = [52.162853,4.4826858];
// startMarker = L.marker(startPos).addTo(map).bindPopup("Rijksmuseum van Oudheden");
// endMarker = L.marker(endPos).addTo(map).bindPopup("Wereldmeseum Leiden");

// //Create path
// console.log(startMarker);
// let path = [startMarker.getLatLng()],
// polyline = L.polyline(path, {color: '#7e7e7e'}).addTo(map),

// // Temporarily add arbitrary positions
// neighbourCoords = [[52.16,4.49], [52.159,4.491], [52.16,4.492]],
// neighbourMarkers = [];


// This function initialises the map at the start. It should only be called once at the start
let map = L.map('map', {maxZoom: 19, minZoom:15, maxBounds: [[52.13, 4.455],[52.19, 4.53]], zoom: 17, center: [52.1581218,4.4855674]});
let path;
let detailedPath;

// Show map layer
mapLayer = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);  

//Create circleIcon
circleIcon = L.icon({
iconUrl: 'circle_icon.png',
iconSize: [16, 16],
iconAnchor: [8, 8],
popupAnchor: [8, 8]
});

// Shows the new optimal path (it shows it from the start for now. This is not permanent) and the new blocked roads (called blocked nodes, but they are roads)
function startNewRound() {
    optimalPathLine = L.polyline(optimalPath, {color: '#ffffff'});
    
    // blockedRoads is the list of all roads that can't be traversed due to being blocked
    // let blockedRoads = [[[52.159,4.491],[52.16,4.492]]];
    blockedNodes.forEach(function(blockedRoad) {
        console.log(blockedRoad);
        L.polyline(blockedRoad, {color: '#dd0000'}).addTo(map);
    });

    startMarker = L.marker(start).addTo(map).bindPopup("Start");
    endMarker = L.marker(end).addTo(map).bindPopup("End");
    neighbourMarkers = [];

    showNeighbours();
}


// Shows adjacent neighbours in the map and makes them clickable
function showNeighbours() {
    neighbourMarkers.forEach(function(marker) {marker.remove()});
    neighbourSubpaths = [];

    neighbours.forEach(function(endPoint, subpath, distance) {
        let marker = L.marker(endPoint, {icon: circleIcon}).addTo(map).bindPopup();
        neighbourMarkers.push(marker);
        neighboursubpaths.push(subpath)
        marker.on('click', function(e) {
            path.forEach(function(node) {
                if (e.latlng.equals(node)) {
                    L.polyline([e.latlng, path.at(-1)], {color: '#343434'}).addTo(map);
                }
            });
            detailedPath.pushValues(neighbourSubpaths[neighbourMarkers.index(e)]);
            detailedPath.push([e.latlng[0], e.latlng[1]]);
            path.push(e.latlng);
            polyline.setLatLngs(detailedPath);
            marker.closePopup();
            
            updateDistance(distance);

            if (e.latlng.equals(endMarker.latlng)) {
                optimalPathLine.addTo(map);
                endRound();
            }
            else requestNeighbours([e.latlng[0], e.latlng[1]]);
        });
        
    })
}

