var MapView = Backbone.View.extend({
    initialize: function() {
        this.collection.on("reset", function(events) {
            this.removeMarkers();
            this.setAllMarkers();
        }, this);
    },
    
    id: "map_canvas",
    
    template: Mustache.template('marker').render,
    
    markers: new Array(),
    
    render: function() {
        google.maps.event.addDomListener(window, 'load', function() {
            var myOptions = {
                center: new google.maps.LatLng(37.88397, -122.2644), 
                zoom: 9,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            };

            this.map = new google.maps.Map($("#map_canvas").get(0),
                myOptions);

            google.maps.event.addListener(this.map, 'tilesloaded', function() {
                this.setAllMarkers();
                google.maps.event.clearListeners(this.map, 'tilesloaded');
            }.bind(this));
        }.bind(this));
        
        return this;
    },
    
    setAllMarkers: function() {
        _.each(this.collection.models, function(item, index, items) {
            this.setMarker(item.get("latitude"), 
                            item.get("longitude"), 
                            item.getAddress(), 
                            item.get("category"),
                            this.template(item.toJSON()));
        }, this);
    },
    
    setMarker: function(latitude, longitude, address, category, info) {

        var image = '/static/img/pin-map-' + category + '.png';

        var infoWindow = new google.maps.InfoWindow({
            content: info
        });

        var location = new google.maps.LatLng(latitude, longitude);
        this.map.setCenter(location);
        
        var marker = new google.maps.Marker({
            map: this.map,
            draggable: false,
            position: location,
            icon: image,
            title : address,
            animation: google.maps.Animation.DROP,
        });

        google.maps.event.addListener(marker, 'click', function() {
            infoWindow.close();
            infoWindow.open(this.map,marker);
        }.bind(this));

        this.markers.push(marker);
    },
    
    removeMarkers: function() {
        _.each(this.markers, function(marker, index, markers) {
            marker.setMap(null);
        }, this);
    },
});
