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
    iconSize: [20, 20],
    iconAnchor: [10, 10],
    popupAnchor: [10, 10]
});

//Create startIcon
startIcon = L.icon({
    iconUrl: 'start_marker_icon.png',
    iconSize: [32, 48],
    iconAnchor: [16, 48],
    popupAnchor:  [16, 48]
});

//Create endIcon
endIcon = L.icon({
    iconUrl: 'end_marker_icon.png',
    iconSize: [32, 48],
    iconAnchor: [16, 48],
    popupAnchor:  [16, 48]
});


// Shows the new optimal path (it shows it from the start for now. This is not permanent) and the new blocked roads (called blocked nodes, but they are roads)
function startNewRound() {
    optimalPathLine = L.polyline(optimalPath, {color: '#78a100'});
    // optimalPathLine.addTo(map);
    blockedRoadsFeatureGroup = L.featureGroup();
    // blockedEdges is an array with the start and end points of the blocked roads
    blockedEdges = [];
    for (blockedRoad of blockedRoads) {
        if (difficulty != 100) {
            blockedRoadsFeatureGroup.addLayer(L.polyline(blockedRoad, {color: '#dd0000'}));
        }
        blockedEdges.push([blockedRoad[0], blockedRoad[blockedRoad.length-1]])
    }
    blockedRoadsFeatureGroup.addTo(map);

    startMarker = L.marker(start, {icon: startIcon, zIndexOffset: -1000}).addTo(map).bindPopup("Start");
    endMarker = L.marker(end, {icon: endIcon, zIndexOffset: -999}).addTo(map).bindPopup("End");
    neighbourMarkers = [];

    path = [startMarker.getLatLng()];
    detailedPath = [];

    pathLine = L.polyline(detailedPath, {color: '#2e80d1'}).addTo(map);
    currentPosition = start;
    requestNeighbours(start);
    // console.log(startMarker.getLatLng(), endMarker.getLatLng());
    map.fitBounds([startMarker.getLatLng(), endMarker.getLatLng()], {padding: [0.4, 0.4]});
}

function clearMap() {
    optimalPathLine.remove();
    startMarker.remove();
    endMarker.remove();
    blockedRoadsFeatureGroup.clearLayers();
    pathLine.remove();
    neighbourMarkers.forEach(function(marker) {marker.remove()});
    // requestNeighbours(start);
    console.log("Cleared map")
}
// function clearMap() {
//     // Remove the optimal path line
//     if (optimalPathLine) {optimalPathLine.remove();}

//     // Remove the start marker
//     if (startMarker) {startMarker.remove();}

//     // Remove the end marker
//     if (endMarker) {endMarker.remove();}

//     // Clear the blocked roads feature group
//     if (blockedRoadsFeatureGroup) {
//         blockedRoadsFeatureGroup.clearLayers();
//     }

//     // Remove the path line
//     if (pathLine) {pathLine.remove();}

//     // Remove all neighbour markers
//     if (neighbourMarkers && neighbourMarkers.length > 0) {
//         neighbourMarkers.forEach(function(marker) {
//             marker.remove();
//         });}

//     // Reset the variables
//     neighbourMarkers = [];
//     path = [];
//     detailedPath = [];
// }

// Shows adjacent neighbours in the map and makes them clickable
function showNeighbours() {
    neighbourMarkers.forEach(function(marker) {marker.remove()});
    neighbourMarkers = [];
    let neighbourSubpaths = [];
    // console.log("blockedEdges",blockedEdges)
    for (trio of neighbours) {
        let endPoint = trio[0],
        subpath = trio[1],
        distance = trio[2];
        console.log("edge:",[currentPosition, endPoint], "distance:", distance);

        let edgeBlocked = false
        for (blockedEdge of blockedEdges) {
            if ((blockedEdge[0][0] == currentPosition[0] && blockedEdge[0][1] == currentPosition[1]) && (blockedEdge[1][0] == endPoint[0] && blockedEdge[1][1] == endPoint[1])
                || (blockedEdge[1][0] == currentPosition[0] && blockedEdge[1][1] == currentPosition[1]) && (blockedEdge[0][0] == endPoint[0] && blockedEdge[0][1] == endPoint[1])) {
                edgeBlocked = true
                if (difficulty == 100) {
                    blockedRoadsFeatureGroup.addLayer(L.polyline(subpath, {color: '#dd0000'}));
                }
                break
            }
        }

        if (!edgeBlocked) {
            let marker = L.marker([parseFloat(endPoint[0]), parseFloat(endPoint[1])], {icon: circleIcon}).addTo(map).bindPopup("");
            neighbourMarkers.push(marker);
            neighbourSubpaths.push(subpath);
            marker.on('click', function(e) {
                let i = 0;
                for (neighbourMarker of neighbourMarkers) {
                    if (neighbourMarker.getLatLng().equals(e.latlng)) {
                        for (subnode of neighbourSubpaths[i]) {detailedPath.push(subnode)};
                        break;
                    }
                    i++;
                }
                currentPosition = [e.latlng.lat, e.latlng.lng];
                path.push(e.latlng);
                pathLine.setLatLngs(detailedPath);
                marker.closePopup();
                
                updateDistance(distance);

                if (e.latlng.equals(end)) {
                    optimalPathLine.addTo(map);
                    neighbourMarkers.forEach(function(marker) {marker.remove()});
                    endRound();
                }
                else {
                    requestNeighbours([e.latlng["lat"], e.latlng["lng"]]);
                }
            })
        }

    }
}
