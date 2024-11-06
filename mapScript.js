$(document).ready(function() {
    // Initialise map
    let map = L.map('map').setView([52.16, 4.49], 14);
    
    // // Google streets map
    // let googleStreets = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',{
    // maxZoom: 20,
    // subdomains:['mt0','mt1','mt2','mt3']
    // });
    // googleStreets.addTo(map);

    // Show map layer
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    bounds: [[52,4],[52.3,5]]
    }).addTo(map);  

    // Add start and end positions and put their markers
    let startPos = [52.1581218,4.4855674],
    endPos = [52.162853,4.4826858];
    startMarker = L.marker(startPos).addTo(map).bindPopup("Rijksmuseum van Oudheden");
    endMarker = L.marker(endPos).addTo(map).bindPopup("Wereldmeseum Leiden");
    
    // Declare score variable
    let score = 0;

    //Create circleIcon
    var circleIcon = L.icon({
    iconUrl: 'circle_icon.png',
    iconSize: [16, 16],
    iconAnchor: [8, 8],
    popupAnchor: [8, 8]
    });

    //Create path
    console.log(startMarker);
    let path = [startMarker.getLatLng()];
    var polyline = L.polyline(path, {color: 'red'}).addTo(map);

    // Temporarily add arbitrary positions
    let markers = [],
    coordinates = [[52.16,4.49], [52.159,4.491], [52.16,4.492]];

    // Make markers with these positions, with an event that makes it so that you can add them to the path
    // by clicking on then
    coordinates.forEach(function(coords) {
        let marker = L.marker(coords, {icon: circleIcon}).on('click', function(e) {
            console.log(path);
            path.push(e.latlng);
            polyline.setLatLngs(path);
            score++;
            //Does not work
            $('#score').val(score);
        });
        markers.push(marker);
    });

    let adjNodeGroup = L.featureGroup(markers).addTo(map).bindPopup();

    // Make undo button
    $(document).on('click', '#undo', function() {
        path.pop();
        polyline.setLatLngs(path);
    });
});