var MapView = Backbone.View.extend({
    initialize: function() {
        this.collection.on("reset", function(events) {
            if (this.map != null)
            {
                this.removeMarkers();
                this.setAllMarkers();
            }
        }, this);
        
        this.collection.on("remove", function(evt, collection, options) {
            this.destroyMarker(options.index);
        }, this);
    },
    
    id: "map_canvas",
    
    template: Mustache.template('marker').render,
    
    markers: new Array(),
    
    location: new google.maps.LatLng(37.88397, -122.2644),
    
    render: function() {
        google.maps.event.addDomListener(window, 'load', function() {
            var myOptions = {
                center: this.location,
                zoom: 9,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            };

            this.map = new google.maps.Map($("#map_canvas").get(0),
                myOptions);

            navigator.geolocation.getCurrentPosition(this.foundUserLocation.bind(this),this.noUserLocation.bind(this),{timeout:10000});

            google.maps.event.addListener(this.map, 'tilesloaded', function() {
                this.map.setCenter(this.location);
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
    
    destroyMarker: function(index) {
        this.markers[index].setMap(null);
        this.markers.splice(index, 1);
    },
    
    foundUserLocation: function(position) {
        this.location = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
        
        if (this.map != null)
        {
            this.map.setCenter(this.location);
        }
    },
    
    noUserLocation: function() {
    }
});
