var MapView = Backbone.View.extend({
    initialize: function() {
        this.mapLoaded = false;
        this.eventsLoaded = false;
    
        this.collection.on("reset", function(events) {
            this.eventsLoaded = true;
            if (this.mapLoaded === true) {
                this.removeMarkers();
                this.setAllMarkers();
            }
        }, this);

        this.collection.on("remove", function(evt, collection, options) {
            this.destroyMarker(options.index);
        }, this);
        
        if (this.mobile) {
            this.popUpTemplate = Mustache.template('m-map-popup').render;
            this.infoWindow.setOptions({maxWidth: 200});
            this.mapOptions.zoomControl = false;
        }
        else {
            this.popUpTemplate = Mustache.template('map-popup').render;
            this.hoverTemplate = Mustache.template('pin-hover').render;
            this.mapOptions.zoomControl = true;
            this.mapOptions.zoomControlOptions = {position: google.maps.ControlPosition.LEFT_CENTER};
        }
    },

    id: "map_canvas",
    
    markers: [],
    
    mobile: $.cookie('flavour') == 'mobile',
    
    userLocation: new google.maps.LatLng(37.88397, -122.2644),

    mapLocation: new google.maps.LatLng(37.88397, -122.2644),

    mapOptions: {
            zoom: 13,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            mapTypeControl: false,
            panControl: false,
            zoomControl: false
    },

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
        
        google.maps.visualRefresh = true;
    },
    
    getCurrentPosition: function() {
        navigator.geolocation.getCurrentPosition(this.foundUserLocation.bind(this),this.noUserLocation.bind(this),{timeout:5000});
    },

    loadMap: function() {
        this.mapOptions.center = this.mapLocation;
    
        this.map = new google.maps.Map($("#map_canvas").get(0),
            this.mapOptions);

        //Listen for tiles loaded
        google.maps.event.addListener(this.map, 'tilesloaded', function() {
            google.maps.event.clearListeners(this.map, 'tilesloaded');
            this.mapLoaded = true;
            
            this.overlay.draw = function() {};
            this.overlay.setMap(this.map);
            
            this.setMapLocation(true);
            $('#map-latitude').change();
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
            this.setMapLocation(false);
            
            if (this.hasVisibleMarkers === false) {
                $('#map-latitude').change();
            }
        }.bind(this));

        google.maps.event.addListener(this.map, 'zoom_changed', function() {
            if ($('#map-radius').length) {
                $('#map-radius').val(parseFloat(this.mapRadius()));
            }
            
            this.setMapLocation(false);
            
            if (this.hasVisibleMarkers === false) {
                $('#map-latitude').change();
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
        console.log('setting marker with name: ' + event.get('name'));
        var image = {
						url: '/static/img/data/pin-' + category + '.svg',
						size: new google.maps.Size(31, 32, 'px', 'px')
					};

        var location = new google.maps.LatLng(latitude, longitude);

        var marker = new google.maps.Marker({
            map: this.map,
            icon: image,
            position: location,
            animation: google.maps.Animation.DROP
        });

        google.maps.event.addListener(marker, 'click', function() {
            this.infoWindow.close();
            this.infoWindow.setContent(info);
            this.infoWindow.open(this.map, marker);
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
        
        if (!this.mobile) {
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
        }

        event.on('open', openMarker);
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
        if (this.markers.length > 0) {
            _.each(this.markers, function(marker, index, markers) {
                marker.setMap(null);
                marker.hoverInfo = null;
            }, this);
            
            this.markers = [];
        }
    },

    destroyMarker: function(index) {
        this.markers[index].setMap(null);
        this.markers[index].hoverInfo = null;
        this.markers[index] = null;
        this.markers.splice(index, 1);
    },

    setMapLocation: function(setToUserLocation) {
        if ($('#map-latitude').length && $('#map-longitude').length) {
            if (setToUserLocation || ($('#map-latitude').val() === "0" && $('#map-longitude').val() === "0")) {
                this.mapLocation = this.userLocation;
            }
            else {
                this.mapLocation = new google.maps.LatLng($('#map-latitude').val(), $('#map-longitude').val());
            }
        }

        if (this.map !== undefined) {
            this.centerMap(this.mapLocation);
        }

        this.hasVisibleMarkers = false;
        _.each(this.collection.models, function(item, index, items) {
            var latLng = new google.maps.LatLng(item.get('latitude'),
                                                item.get('longitude'));
            if (this.map.getBounds().contains(latLng)) {
                this.hasVisibleMarkers = true;
            }
        }, this);
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
            this.setMapLocation(true);
        }
        else {
            this.setMapLocation(false);
        }

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
