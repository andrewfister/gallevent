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

    popUpTemplate: Mustache.template('map-popup').render,
    
    hoverTemplate: Mustache.template('pin-hover').render,

    markers: [],
    
    userLocation: new google.maps.LatLng(37.88397, -122.2644),

    mapLocation: new google.maps.LatLng(37.88397, -122.2644),

    infoWindow: new google.maps.InfoWindow(),

    overlay: new google.maps.OverlayView(),
    
    geocoder: new google.maps.Geocoder(),

    render: function() {
        $('#location-search-input').keypress(function(event) {
            if (event.which === 13) {
                this.locationSearch();
            }
        }.bind(this));
        
        $('#location-search-button').click(function(event) {
            this.locationSearch();
        }.bind(this));
        
        $('#my-location').click(function(event) {
            this.getCurrentPosition();
        }.bind(this));
    
        this.getCurrentPosition();
    },
    
    getCurrentPosition: function() {
        navigator.geolocation.getCurrentPosition(this.foundUserLocation.bind(this),this.noUserLocation.bind(this),{timeout:5000});
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
            
            this.overlay.draw = function() {};
            this.overlay.setMap(this.map);
        }.bind(this));

        google.maps.event.addListener(this.map, 'dragend', function(data) {
            var center = this.map.getCenter();
            var lat = parseFloat(center.lat());
            var lon = parseFloat(center.lng());
            if ($('#map-latitude').length) {
                $('#map-latitude').val(lat);
            }
            if ($('#map-longitude').length) {
                $('#map-longitude').val(lon);
            }
            this.setMapLocation();
        }.bind(this));

        google.maps.event.addListener(this.map, 'zoom_changed', function() {
            if ($('#map-radius').length) {
                $('#map-radius').val(parseFloat(this.mapRadius()));
            }
        }.bind(this));

        return this;
    },
    
    locationSearch: function() {
        this.geocoder.geocode({ address: $('#location-search-input').val() }, function(results, status) {
            if (status === google.maps.GeocoderStatus.OK) {
                var newLocation = results[0].geometry.location;
                this.centerMap(newLocation);
                $('#map-longitude').change();
            }
            else {
                alert("Could not find your location at the moment!");
            }
        }.bind(this));
    },
    
    setAllMarkers: function() {
        _.each(this.collection.models, function(item, index, items) {
            this.setMarker(item, item.get("latitude"),
                            item.get("longitude"),
                            item.getAddress(),
                            item.get("category"),
                            this.popUpTemplate(item.toJSON()));
        }, this);
    },

    setMarker: function(event, latitude, longitude, address, category, info) {
        var image = '/static/img/data/pin-' + category + '-31x32.svg';

        var location = new google.maps.LatLng(latitude, longitude);

        var marker = new google.maps.Marker({
            map: this.map,
            draggable: false,
            position: location,
            icon: image,
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
        this.setMarkerHover(marker, event);

        google.maps.event.addListener(marker, 'mouseover', function() {
            $(marker.hoverInfo).removeClass('hidden');
        }.bind(this));
        
        google.maps.event.addListener(marker, 'mouseout', function() {
            $(marker.hoverInfo).addClass('hidden');
        }.bind(this));
        
        google.maps.event.addListener(this.map, 'zoom_changed', function() {
            this.setMarkerHover(marker, event);
        }.bind(this));
        
        google.maps.event.addListener(this.map, 'dragend', function() {
            this.setMarkerHover(marker, event);
        }.bind(this));

        event.on('open', openMarker);
        event.trigger('pinDropped');
    },

    setMarkerHover: function(marker, event) {
        marker.hoverInfo = $(this.hoverTemplate(event.toJSON()))[0];
        
        if (this.mapPanes === undefined) {
            this.mapPanes = this.overlay.getPanes();
        }
        this.mapPanes.overlayMouseTarget.appendChild(marker.hoverInfo);
        var projection = this.overlay.getProjection();
        if (projection) {
            var markerLatLng = marker.getPosition();
            var markerPosition = projection.fromLatLngToDivPixel(markerLatLng);
            marker.hoverInfo.style.left = (markerPosition.x + 25) + 'px';
            marker.hoverInfo.style.top = (markerPosition.y - 30) + 'px';
        }
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

    setMapLocation: function(setToUserLpcation = false) {
        if ($('#map-latitude').length && $('#map-longitude').length) {
            if (setToUserLpcation || ($('#map-latitude').val() === "0" && $('#map-longitude').val() === "0")) {
                this.mapLocation = this.userLocation;
            }
            else {
                this.mapLocation = new google.maps.LatLng($('#map-latitude').val(), $('#map-longitude').val());
            }
        }

        if (this.map !== undefined) {
            this.centerMap(this.mapLocation);
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

        var userLatitude = parseFloat(this.userLocation.lat());
        var userLongitude = parseFloat(this.userLocation.lng());

        //Set user location data on page and in cookie
        if ($('#user-latitude').length)
        {
            $('#user-latitude').html(userLatitude);
            $.cookie('user-latitude', userLatitude, { expires: 1, path: '/' });
        }
        if ($('#user-longitude').length)
        {
            $('#user-longitude').html(userLongitude);
            $.cookie('user-longitude', userLongitude, { expires: 1, path: '/' });
        }

        this.setMapLocation(true);

        this.loadMap();
    },

    noUserLocation: function() {
        var userLatitude = $.cookie('user-latitude');
        var userLongitude = $.cookie('user-longitude');

        if (userLatitude != null && userLongitude != null)
        {
            this.userLocation = new google.maps.LatLng(userLatitude, userLongitude);
        }

        this.setMapLocation(true);

        this.loadMap();
    },

    centerMap: function(latLng) {
        if (this.map !== null  && this.map !== undefined)
        {
            this.map.setCenter(latLng);
        }

        var mapLatitude = parseFloat(latLng.lat());
        var mapLongitude = parseFloat(latLng.lng());

        //Set map data
        if ($('#map-latitude').length) {
            $('#map-latitude').val(mapLatitude);
        }
        if ($('#map-longitude').length) {
            $('#map-longitude').val(mapLongitude);
        }
        if ($('#map-radius').length) {
            $('#map-radius').val(parseFloat(this.mapRadius()));
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
