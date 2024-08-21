var map = L.map('map', {
    zoomControl: false,
    dragging: false,
    scrollWheelZoom: false,
    doubleClickZoom: false,
    touchZoom: false
});

// Remove any base layer since we want a white background only
// No tileLayer is added

// Load GeoJSON from an external file
fetch('michigan_counties.geojson')
    .then(response => response.json())
    .then(data => {
        var geoJsonLayer = L.geoJson(data, {
            style: {
                color: '#000000',  // Boundary line color
                weight: 2,  // Boundary line width
                fillOpacity: 0  // No fill
            },
            onEachFeature: onEachFeature
        }).addTo(map);

        // Automatically adjust the view to show all features
        map.fitBounds(geoJsonLayer.getBounds());
    });

function onEachFeature(feature, layer) {
    var size = 100;  // Modify this based on your actual data attribute
    var center = layer.getBounds().getCenter();
    var circle = L.circle(center, {
        radius: size * 100,  // Scale size appropriately
        fillColor: 'blue',
        fillOpacity: 0.5,
        stroke: false
    }).addTo(map);

    circle.bindPopup(`County: ${feature.properties.Name}<br>Harris Votes Remaining: ${size}<br>Trump Votes Remaining: ${size}`);
}
