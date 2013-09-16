var MapView = Backbone.View.extend({
    initialize: function() {
        this.collection.on("reset", function(events) {
            if (this.map !== null)
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

    markers: [],
    
    categoryCounts: {},

    userLocation: new google.maps.LatLng(37.88397, -122.2644),

    mapLocation: new google.maps.LatLng(37.88397, -122.2644),

    infoWindow: new google.maps.InfoWindow(),

    render: function() {
        navigator.geolocation.getCurrentPosition(this.foundUserLocation.bind(this),this.noUserLocation.bind(this),{timeout:10000});
    },

    loadMap: function() {
        var myOptions = {
            center: this.mapLocation,
            zoom: 13,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            mapTypeControl: false,
            panControl: false,
            zoomControlOptions: {position: google.maps.ControlPosition.LEFT_CENTER}
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
            if ($('#map-latitude').length)
            {
                $('#map-latitude').attr('value', lat);
            }
            if ($('#map-longitude').length)
            {
                $('#map-longitude').attr('value', lon);
            }
            this.setMapLocation();
        }.bind(this));

        google.maps.event.addListener(this.map, 'zoom_changed', function() {
            if ($('#map-radius').length) {
                $('#map-radius').attr('value', parseFloat(this.mapRadius()));
            }
        }.bind(this));

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
            animation: google.maps.Animation.DROP
        });

        google.maps.event.addListener(marker, 'click', function() {
            this.infoWindow.close();
            this.infoWindow.setContent(info);
            this.infoWindow.open(this.map,marker);
        }.bind(this));

        this.markers.push(marker);

        var makeOpenMarker = function(marker, infoWindow, map)
        {
            return function() {
                infoWindow.close();
                infoWindow.setContent(info);
                infoWindow.open(map,marker);
            };
        };

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

    setMapLocation: function() {
        if ($('#map-latitude').length && $('#map-longitude').length)
        {
            if ($('#map-latitude').attr('value') === "0" && $('#map-longitude').attr('value') === "0")
            {
                this.mapLocation = this.userLocation;
                if ($('#map-latitude').length) {
                    $('#map-latitude').attr('value', this.mapLocation.lat());
                }
                if ($('#map-longitude').length) {
                    $('#map-longitude').attr('value', this.mapLocation.lng());
                }
            }
            else
            {
                this.mapLocation = new google.maps.LatLng($('#map-latitude').attr('value'), $('#map-longitude').attr('value'));
            }
        }

        var hasVisibleMarkers = false;

        _.each(this.collection.models, function(item, index, items) {
            var latLng = new google.maps.LatLng(item.get('latitude'),
                                                item.get('longitude'));
            if (this.map.getBounds().contains(latLng)) {
                hasVisibleMarkers = true;
            }
        }, this);

        if (hasVisibleMarkers === false) {
            $('#map-latitude').change();
        }
    },

    foundUserLocation: function(position) {
        this.userLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);

        var mapLatitude = parseFloat(this.userLocation.lat());
        var mapLongitude = parseFloat(this.userLocation.lng());

        //Set user location data on page and in cookie
        if ($('#user-latitude').length)
        {
            $('#user-latitude').html(mapLatitude);
            $.cookie('user-latitude', mapLatitude, { expires: 365, path: '/' });
        }
        if ($('#user-longitude').length)
        {
            $('#user-longitude').html(mapLongitude);
            $.cookie('user-longitude', mapLongitude, { expires: 365, path: '/' });
        }

        this.setMapLocation();

        this.loadMap();
    },

    noUserLocation: function() {
        var userLatitude = $.cookie('user-latitude');
        var userLongitude = $.cookie('user-longitude');

        if (userLatitude.length && userLongitude.length)
        {
            this.userLocation = new google.maps.LatLng(userLatitude, userLongitude);
        }

        this.setMapLocation();

        this.loadMap();
    },

    centerMap: function(latLng) {
        if (this.map !== null)
        {
            this.map.setCenter(latLng);
        }

        var mapLatitude = parseFloat(latLng.lat());
        var mapLongitude = parseFloat(latLng.lng());

        //Set map data
        if ($('#map-latitude').length) {
            $('#map-latitude').attr('value', mapLatitude);
        }
        if ($('#map-longitude').length) {
            $('#map-longitude').attr('value', mapLongitude);
        }
        if ($('#map-radius').length) {
            $('#map-radius').attr('value', parseFloat(this.mapRadius()));
        }
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
    }
});
