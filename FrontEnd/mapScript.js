// Initialise the map
let map = L.map('map', {maxZoom: 18, minZoom:15, maxBounds: [[52.13, 4.455],[52.19, 4.53]], zoom: 15, center: [52.1581218,4.4855674]});

// Create the map layer and add it to the map
mapLayer = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);  

// Create circleIcon
circleIcon = L.icon({
    iconUrl: 'circle_icon.webp',
    iconSize: [20, 20],
    iconAnchor: [10, 10],
    popupAnchor: [10, 10]
});

// Create startIcon
startIcon = L.icon({
    iconUrl: 'start_marker_icon.webp',
    iconSize: [32, 48],
    iconAnchor: [16, 48],
    popupAnchor:  [16, 48]
});

// Create endIcon
endIcon = L.icon({
    iconUrl: 'end_marker_icon.webp',
    iconSize: [32, 48],
    iconAnchor: [16, 48],
    popupAnchor:  [16, 48]
});

// Create playerIcon
playerIcon = L.icon({
    iconUrl: 'player_icon.webp',
    iconSize: [10, 10],
    iconAnchor: [5, 5],
    popupAnchor: [5, 5]
});


// This function declares the necessary variables for the display and functionality of lines and nodes in the map. It is passed  at the start of a round
function startNewRound() {
    optimalPathLine = L.polyline(optimalPath, {color: '#78a100'});
    blockedRoadsFeatureGroup = L.featureGroup();
    blockedEdges = [];

    // Add the start and end position of each blocked road to blockedEdges. In the normal difficulty, also paint the blocked roads on the map
    for (blockedRoad of blockedRoads) {
        if (difficulty == 50) {
            blockedRoadsFeatureGroup.addLayer(L.polyline(blockedRoad, {color: '#dd0000'}));
        }
        blockedEdges.push([blockedRoad[0], blockedRoad[blockedRoad.length-1]])
    }
    blockedRoadsFeatureGroup.addTo(map);

    startMarker = L.marker(start, {icon: startIcon, zIndexOffset: -1000}).addTo(map).bindPopup("Start");
    endMarker = L.marker(end, {icon: endIcon, zIndexOffset: -999}).addTo(map).bindPopup("End");

    // The path represents the list of nodes through which the user has passed
    // The detailed path contains all the subnodes going from node to node in order to create a more detailed path with curves
    path = [startMarker.getLatLng()];
    detailedPath = [];

    pathLine = L.polyline(detailedPath, {color: '#2e80d1'}).addTo(map);
    currentPosition = start;
    neighbourMarkers = [];
    playerMarker = L.marker([0,0]);
    requestNeighbours(start);

    // Set the view so the start and end nodes both on screen
    map.fitBounds([startMarker.getLatLng(), endMarker.getLatLng()], {padding: [0.4, 0.4]});
}

// Clear the variables from the map so that they can be remade in the new round
function clearMap() {
    optimalPathLine.remove();
    startMarker.remove();
    endMarker.remove();
    blockedRoadsFeatureGroup.clearLayers();
    pathLine.remove();
    neighbourMarkers.forEach(function(marker) {marker.remove()});
    console.log("Cleared map")
}

// This function creates markers that represent all the adjacent nodes (neighbours)
function showNeighbours() {
    // Remove all the existing markers for neighbours
    playerMarker.remove();
    neighbourMarkers.forEach(function(marker) {marker.remove()});
    playerMarker = L.marker(currentPosition, {icon: playerIcon}).addTo(map).bindPopup("Current position");
    neighbourMarkers = [];
    let neighbourSubpaths = [];

    for (trio of neighbours) {
        let endPoint = trio[0],
        subpath = trio[1],
        distance = trio[2];

        // Check if the edge appears in the blockedEdges list
        edgeBlocked = false;
        for (blockedEdge of blockedEdges) {
            if ((blockedEdge[0][0] == currentPosition[0] && blockedEdge[0][1] == currentPosition[1]) && (blockedEdge[1][0] == endPoint[0] && blockedEdge[1][1] == endPoint[1])
                || (blockedEdge[1][0] == currentPosition[0] && blockedEdge[1][1] == currentPosition[1]) && (blockedEdge[0][0] == endPoint[0] && blockedEdge[0][1] == endPoint[1])) {
                edgeBlocked = true;
                // In hard mode, paint the blocked road going to this neighbour
                if (difficulty == 100) {
                    blockedRoadsFeatureGroup.addLayer(L.polyline(subpath, {color: '#dd0000'}));
                }
                break
            }
        }
        
        // If the edge going to this neighbour is not blocked, create its marker
        if (!edgeBlocked) {
            let marker = L.marker([parseFloat(endPoint[0]), parseFloat(endPoint[1])], {icon: circleIcon}).addTo(map).bindPopup("");
            neighbourMarkers.push(marker);
            neighbourSubpaths.push(subpath);
            marker.on('click', function(e) {
                // When a marker is clicked, look for this marker in neighbourMarkers and add all its subnodes to the detailed path
                let i = 0;
                for (neighbourMarker of neighbourMarkers) {
                    if (neighbourMarker.getLatLng().equals(e.latlng)) {
                        for (subnode of neighbourSubpaths[i]) {detailedPath.push(subnode)};
                        break;
                    }
                    i++;
                }

                // Update the position and add the neighbour to the map. Display a updated path line on the map
                currentPosition = [e.latlng.lat, e.latlng.lng];
                path.push(e.latlng);
                pathLine.setLatLngs(detailedPath);
                marker.closePopup();
                
                updateDistance(distance);

                // If the clicked-on marker is at the end position, show the optimal path line, remove all the currently shown neighbours and end the round
                if (e.latlng.equals(end)) {
                    optimalPathLine.addTo(map);
                    neighbourMarkers.forEach(function(marker) {marker.remove()});
                    playerMarker.remove();
                    endRound();
                }
                // Otherwise, request neighbours for the new position
                else {
                    requestNeighbours([e.latlng["lat"], e.latlng["lng"]]);
                }
            })
        }

    }
}
