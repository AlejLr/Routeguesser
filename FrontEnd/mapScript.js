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
let map = L.map('map', {maxZoom: 18, minZoom:15, maxBounds: [[52.13, 4.455],[52.19, 4.53]], zoom: 15, center: [52.1581218,4.4855674]});

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

//Create startIcon
startIcon = L.icon({
    iconUrl: 'start_marker_icon.png',
    iconSize: [32, 48],
    iconAnchor: [16, 24],
    popupAnchor:  [16, 24]
});

//Create endIcon
endIcon = L.icon({
    iconUrl: 'end_marker_icon.png',
    iconSize: [32, 48],
    iconAnchor: [16, 24],
    popupAnchor:  [16, 24]
});

// Shows the new optimal path (it shows it from the start for now. This is not permanent) and the new blocked roads (called blocked nodes, but they are roads)
function startNewRound() {
    optimalPathLine = L.polyline(optimalPath, {color: '#78a100'});
    console.log("optimalPath:", optimalPath);
    // blockedRoads is the list of all roads that can't be traversed due to being blocked
    // let blockedRoads = [[[52.159,4.491],[52.16,4.492]]];
    for (blockedRoad of blockedNodes) {
        // console.log(blockedRoad);
        L.polyline(blockedRoad, {color: '#dd0000'}).addTo(map);
    }

    startMarker = L.marker(start).addTo(map).bindPopup("Start");
    endMarker = L.marker(end, {icon: endIcon}).addTo(map).bindPopup("End");
    neighbourMarkers = [];

    path = [startMarker.getLatLng()];
    detailedPath = [];

    pathLine = L.polyline(detailedPath, {color: '#2e80d1'}).addTo(map);

    console.log(neighbours);
    showNeighbours(path, detailedPath);
}


// Shows adjacent neighbours in the map and makes them clickable
function showNeighbours() {
    neighbourMarkers.forEach(function(marker) {marker.remove()});
    neighbourMarkers = [];
    let neighbourSubpaths = [];
    for (trio of neighbours) {
        let endPoint = trio[0],
        subpath = trio[1],
        distance = trio[2];
        console.log(trio)
        // console.log("Neighbour:", endPoint, subpath, distance);
        let marker = L.marker([parseFloat(endPoint[0]), parseFloat(endPoint[1])], {icon: circleIcon}).addTo(map).bindPopup("");
        neighbourMarkers.push(marker);
        neighbourSubpaths.push(subpath);
        // console.log("subpath: ",neighbourSubpaths);
        marker.on('click', function(e) {
            // console.log("neighbourMarkers:", neighbourMarkers);
            // console.log("neighbourSubpaths:", neighbourSubpaths);
            let i = 0;
            for (neighbourMarker of neighbourMarkers) {
                if (neighbourMarker.getLatLng().equals(e.latlng)) {
                    for (subnode of neighbourSubpaths[i]) {detailedPath.push(subnode)};
                    break;
                }
                i++;
            }
            // detailedPath.push([e.latlng.lat, e.latlng.lng]);
            path.push(e.latlng);
            // console.log("detailedPath:", detailedPath);
            // console.log("path:", path);
            pathLine.setLatLngs(detailedPath);
            marker.closePopup();
            
            updateDistance(distance);

            if (e.latlng.equals(endMarker.latlng)) {
                optimalPathLine.addTo(map);
                endRound();
            }
            else {
                requestNeighbours([e.latlng["lat"], e.latlng["lng"]]);
            }
        });

    }
}

// Alex testing spot

function test(){
    optimalPathLine = L.polyline(optimalPath, {color: '#78a100'}).addTo(map);
    console.log("Optimal path: ", optimalPath);
    console.log("Optimal path created");
}