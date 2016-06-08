var map;
var global_markers = [];
var markers =
    [
        [-31.414509, -64.163418,'Centro de Neurología Infantil',''],
        [-31.442897, -64.198562,'Hospital Privado de Córdoba',''],
        [-31.459941, -64.163886,'Hospital Raúl Ferreyra',''],
        [-31.392725, -64.184061,'IPEPGO SRL',''],

        [-31.006666, -64.079772,'Sanatorio Caroya SRL',''],

        [-31.433433, -63.050000,'Clínica del Niño Dr. Costilla',''],

        [-32.413680, -63.245785,'Clínica de Especialidades',''],

        [-29.4153099,-66.8524246,'Centro Médico Vivir',''],

        [-27.790359, -64.260663,'IRIS SRL','']
    ];

var infowindow = new google.maps.InfoWindow({});

function initialize() {
    geocoder = new google.maps.Geocoder();
    var latlng = new google.maps.LatLng(-31.414509, -64.163418);
    var myOptions = {
        zoom: 12,
        center: latlng,
        scrollwheel: false,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    map = new google.maps.Map(document.getElementById("map-canvas"), myOptions);
    addMarker();
}

function addMarker() {
    for (var i = 0; i < markers.length; i++) {
        // obtain the attribues of each marker
        var lat = parseFloat(markers[i][0]);
        var lng = parseFloat(markers[i][1]);
        var trailhead_name = markers[i][2];
        var trailhead_img  = markers[i][3];

        var myLatlng = new google.maps.LatLng(lat, lng);

        var contentString = "<html><body><div><p><h3><b>" + trailhead_name + "</b></h3></p></div></body></html>";

        var marker = new google.maps.Marker({
            position: myLatlng,
            map: map,
            title: trailhead_name
        });

        marker['infowindow'] = contentString;

        global_markers[i] = marker;

        google.maps.event.addListener(global_markers[i], 'click', function() {
            infowindow.setContent(this['infowindow']);
            infowindow.open(map, this);
        });
    }
}

window.onload = initialize;

function goToMarker(idObject) {
    idObject = idObject - 1;
    google.maps.event.trigger(global_markers[idObject], 'click');
    map.setCenter(idObject.getPosition());
}