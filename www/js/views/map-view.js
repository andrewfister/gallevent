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
    
    userLocation: new google.maps.LatLng(37.88397, -122.2644),
    
    mapLocation: new google.maps.LatLng(37.88397, -122.2644),
    
    infoWindow: new google.maps.InfoWindow(),
    
    render: function() {
        navigator.geolocation.getCurrentPosition(this.foundUserLocation.bind(this),this.noUserLocation.bind(this),{timeout:10000});
    },
    
    loadMap: function() {
        //google.maps.event.addDomListener(window, 'load', function() {
            var myOptions = {
                center: this.mapLocation,
                zoom: 13,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            };

            this.map = new google.maps.Map($("#map_canvas").get(0),
                myOptions);

            //Listen for tiles loaded
            google.maps.event.addListener(this.map, 'tilesloaded', function() {
                this.centerMap(this.mapLocation);
                this.setAllMarkers();
                google.maps.event.clearListeners(this.map, 'tilesloaded');
            }.bind(this));
            
            google.maps.event.addListener(this.map, 'dragend', function(data) {
                var center = this.map.getCenter();
                var lat = parseFloat(center.lat());
                var lon = parseFloat(center.lng());
                if ($('#user-latitude').length)
                    $('#user-latitude').attr('value', lat);
                if ($('#user-longitude').length)
                    $('#user-longitude').attr('value', lon);
                this.mapLocation = new google.maps.LatLng(lat, lon);
            }.bind(this));
            
            google.maps.event.addListener(this.map, 'zoom_changed', function() {
                if ($('#map-radius').length)
                    $('#map-radius').attr('value', parseFloat(this.mapRadius()));
            }.bind(this));
        //}.bind(this));
        
        return this;
    },
    
    setAllMarkers: function() {
        _.each(this.collection.models, function(item, index, items) {
            this.setMarker(item, item.get("latitude"), 
                            item.get("longitude"), 
                            item.getAddress(), 
                            item.get("category"),
                            this.template(item.toJSON()));
        }, this);
    },
    
    setMarker: function(event, latitude, longitude, address, category, info) {
        var image = '/static/img/pin-map-' + category + '.png';
        
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
            this.infoWindow.close();
            this.infoWindow.setContent(info);
            this.infoWindow.open(this.map,marker);
        }.bind(this));

        this.markers.push(marker);

        var makeOpenMarker = function(marker, infoWindow, map)
        {
            return  function() {
                infoWindow.close();
                infoWindow.setContent(info);
                infoWindow.open(map,marker);
            }
        }

        var openMarker = makeOpenMarker(marker, this.infoWindow, this.map);
        
        event.on('open', openMarker);
        event.trigger('pinDropped');
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
        this.userLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
        
        if ($('#user-latitude').length && $('#user-longitude').length)
        {
            if ($('#user-latitude').attr('value') == 0 && $('#user-longitude').attr('value') == 0)
            {
                this.mapLocation = this.userLocation;
            }
            else
            {
                this.mapLocation = new google.maps.LatLng($('#user-latitude').attr('value'), $('#user-longitude').attr('value'));
            }
        }
        
        this.loadMap();
    },
    
    noUserLocation: function() {
        this.loadMap();
    },
    
    centerMap: function(latLng) {
        if (this.map != null)
        {
            this.map.setCenter(latLng);
        }
        
        if ($('#user-latitude').length)
            $('#user-latitude').attr('value', parseFloat(latLng.lat()));
        if ($('#user-longitude').length)
            $('#user-longitude').attr('value', parseFloat(latLng.lng()));
        if ($('#map-radius').length)
            $('#map-radius').attr('value', parseFloat(this.mapRadius()));
    },
    
    mapRadius: function(){
        bounds = this.map.getBounds();

        center = bounds.getCenter();
        ne = bounds.getNorthEast();

        // r = radius of the earth in statute miles
        var r = 3963.0;  

        // Convert lat or lng from decimal degrees into radians (divide by 57.2958)
        var lat1 = center.lat() / 57.2958; 
        var lon1 = center.lng() / 57.2958;
        var lat2 = ne.lat() / 57.2958;
        var lon2 = ne.lng() / 57.2958;

        // distance = circle radius from center to Northeast corner of bounds
        return r * Math.acos(Math.sin(lat1) * Math.sin(lat2) + 
            Math.cos(lat1) * Math.cos(lat2) * Math.cos(lon2 - lon1));
    },
});
