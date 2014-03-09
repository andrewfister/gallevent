var MapView = Backbone.View.extend({
    initialize: function() {
        this.mapLoaded = false;
        this.eventsLoaded = false;
        this.markersLoaded = false;
        this.hasVisibleMarkers = false;
    
        this.collection.on("reset", function(events) {
		if(this.mapLoaded){
		    this.loadMarkers();
		}
            this.eventsLoaded = true;
            if (!this.markersLoaded && this.mapLoaded) {
                this.loadMarkers();
            }
        }, this);

        this.collection.on("remove", function(evt, collection, options) {
            this.destroyMarker(options.index);
        }, this);
        
        window.dispatcher.on("fetch", function(evt, collection, options) {
            this.eventsLoaded = false;
            this.markersLoaded = false;
        }, this);
        
        this.hoverTemplate = Mustache.template('pin-hover').render;
        this.popUpTemplate = Mustache.template('map-popup').render;
        this.infoWindow.setOptions({maxWidth: 220});
        this.mapOptions.zoomControl = true;
        this.mapOptions.zoomControlOptions = {position: google.maps.ControlPosition.LEFT_CENTER};
        this.render();

        this.HoverTooltip = function(options) {
            this.marker = options.marker;
            this.map = options.map;
            this.setMap(this.map);
                    
            google.maps.event.addListener(this.marker, 'mouseover', function() {
                $(this.marker.hoverInfo).removeClass('hidden');
            }.bind(this));
            
            google.maps.event.addListener(this.marker, 'mouseout', function() {
                $(this.marker.hoverInfo).addClass('hidden');
            }.bind(this));
        };
        
        this.HoverTooltip.prototype = new google.maps.OverlayView();
        this.HoverTooltip.prototype.onAdd = function() {
            var mapPanes = this.getPanes();
            mapPanes.floatPane.appendChild(this.marker.hoverInfo);
        };
        
        this.HoverTooltip.prototype.draw = function() {
            this.projection = this.getProjection();
            if (this.projection) {
                var markerLatLng = this.marker.getPosition();
                var markerPosition = this.projection.fromLatLngToDivPixel(markerLatLng);
                this.marker.hoverInfo.style.left = (markerPosition.x + 25) + 'px';
                this.marker.hoverInfo.style.top = (markerPosition.y- 30) + 'px';
            }
        };
        
        this.HoverTooltip.prototype.onRemove = function() {
            mapPanes.floatPane.removeChild(this.marker.hoverInfo);
        };
    },

    id: "map_canvas",
    
    markers: [],

    userLocation: new google.maps.LatLng(37.88397, -122.2644),

    mapLocation: new google.maps.LatLng(37.88397, -122.2644),

    mapOptions: {
            zoom: 13,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            mapTypeControl: false,
            panControl: false
    },

    infoWindow: new google.maps.InfoWindow({
        disableAutoPan: true
    }),
    
    geocoder: new google.maps.Geocoder(),    

    render: function() {
        $('#my-location').click(function(event) {
            $('.loading').removeClass('hidden');
            this.getCurrentPosition();
        }.bind(this));
        
        this.getCurrentPosition();
    },
    
    loadMarkers: function() {
        if (this.mapLoaded === true) {
            this.removeMarkers();
            this.setAllMarkers();
            this.markersLoaded = true;
        }
        else {
            this.markersLoaded = false;
        }
    },
    
    getCurrentPosition: function() {
	    navigator.geolocation.getCurrentPosition(this.foundUserLocation.bind(this),this.noUserLocation.bind(this),{timeout:5000});
    },

    loadMap: function() {
        this.mapLoaded = false;
        this.markersLoaded = false;
        this.mapOptions.center = this.mapLocation;
        this.setMapLatLng(this.mapLocation);
    
        this.map = new google.maps.Map($("#map_canvas").get(0),
            this.mapOptions);
        if (!this.dragging) {
            this.eventsLoaded = false;
            this.markersLoaded = false;
            window.searchView.submitSearch();
        }

        //Listen for tiles loaded
        google.maps.event.addListener(this.map, 'tilesloaded', function() {
            this.mapLoaded = true;
            if (!this.markersLoaded && this.eventsLoaded) {
                this.loadMarkers();
            }
	    //	    this.mapLoaded = true;
        }.bind(this));

        google.maps.event.addListener(this.map, 'dragstart', function(data) {
            this.dragging = true;
        }.bind(this));

        google.maps.event.addListener(this.map, 'dragend', function(data) {
            var center = this.map.getCenter();
            
            this.dragging = false;
            this.setMapLatLng(center);
            this.setMapLocation(false);
        }.bind(this));

        google.maps.event.addListener(this.map, 'zoom_changed', function() {
            var center = this.map.getCenter();
            
            this.setMapLatLng(center);
            this.setMapLocation(false);
            this.setMapRadius();
        }.bind(this));

        google.maps.event.addListener(this.map, 'center_changed', function() {
            if (!this.dragging && !this.detectVisibleMarkers()) {
                this.eventsLoaded = false;
                this.markersLoaded = false;
                window.searchView.submitSearch();
            }
        }.bind(this));
        
        return this;
    },
    
    locationSearch: function(locationAddress) {
        this.geocoder.geocode({ address: locationAddress }, function(results, status) {
            if (status === google.maps.GeocoderStatus.OK) {
                var newLocation = results[0].geometry.location;
                
                this.setMapLatLng(newLocation);
                this.centerMap(newLocation);
            }
        }.bind(this));
    },
    

    addressParse : function(locationAddress, addressComponents) {
	    
	    this.geocoder.geocode({ address: locationAddress }, function(results, status) {
		    if (status === google.maps.GeocoderStatus.OK) {
			var newLocation = results[0].address_components;
			for(var i=0; i<newLocation.length; i++)
			    {
				var component_type = newLocation[i]["types"][0];
				var component_value = newLocation[i]["long_name"][0];

				switch ( component_type )
				    {
				    case "street_number" : 
					addressComponents["street_number"] = component_value; break;
 
				    case "route" :
                                        addressComponents["street"] = component_value; break;

				    case "locality" :
                                        addressComponents["city"] = component_value; break;

				    case "administrative_area_level_1" :
                                        addressComponents["state"] = component_value; break;

				    case "postal_code" :
					addressComponents["zipcode"] = component_value; break;

				    case "country" :
					addressComponents["country"] = component_value; break;

				    default: break;
				    }
			    }
		    }.bind(this)  } ) ;
	}  
			    
	    
    setMapLatLng: function(location) {
        if ($('#map-latitude').length) {
            $('#map-latitude').val(parseFloat(location.lat()));
        }
        if ($('#map-longitude').length) {
            $('#map-longitude').val(parseFloat(location.lng()));
        }
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

        marker.event = event;

        google.maps.event.addListener(marker, 'click', function() {
            this.infoWindow.close();
            this.infoWindow.setContent(info);
            this.map.panTo(marker.getPosition());
            this.map.panBy(0, -150);
            this.infoWindow.open(this.map, marker);
//            this.overlay = new google.maps.OverlayView();
//            this.overlay.draw = function() {};
//            this.overlay.setMap(this.map);
        }.bind(this));

        this.markers.push(marker);

        var makeOpenMarker = function(marker, infoWindow, map)
        {
            return function() {
                infoWindow.close();
                infoWindow.setContent(info);
                infoWindow.open(map, marker);
                this.projection = this.overlay.getProjection();
                if (this.projection) {
                    this.map.panBy(0, this.projection.fromLatLngToDivPixel(marker.getPosition()).y-320);
                }
            }.bind(this);
        }.bind(this);

        var openMarker = makeOpenMarker(marker, this.infoWindow, this.map);
        
        this.setMarkerHover(marker, event);
        
        event.on('open', openMarker);
    },
    
    setMarkerHover: function(marker, event) {
        marker.hoverInfo = $(this.hoverTemplate(marker.event.toJSON()))[0];
        marker.tooltip = new this.HoverTooltip({ marker: marker, map: this.map });
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

        if (this.map !== undefined && !this.map.getCenter().equals(this.mapLocation)) {
            this.centerMap(this.mapLocation);
        }
    },
    
    detectVisibleMarkers: function() {
        this.hasVisibleMarkers = false;
        _.each(this.collection.models, function(item, index, items) {
            var latLng = new google.maps.LatLng(item.get('latitude'),
                                                item.get('longitude'));
            if (this.map.getBounds().contains(latLng)) {
                this.hasVisibleMarkers = true;
            }
        }, this);
        
        return this.hasVisibleMarkers;
    },

    foundUserLocation: function(position) {
        this.userLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);

        var userLatitude = parseFloat(this.userLocation.lat());
        var userLongitude = parseFloat(this.userLocation.lng());
	      
	    localStorage.setItem('user-latitude', userLatitude);
	    localStorage.setItem('user-longitude', userLongitude);

        this.setMapLocation(true);
 
        this.loadMap();
    },

    noUserLocation: function() {
	    //try from local storage
	    userLatitude =localStorage.getItem('user-latitude');
	    userLongitude = localStorage.getItem('user-longitude');
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
        //Set map data
        this.setMapLatLng(latLng);
        this.setMapRadius();
    
        if (this.map !== null && this.map !== undefined)
        {
            this.map.setCenter(latLng);
        }
    },
    
    setMapRadius: function() {
        if ($('#map-radius').length) {
            $('#map-radius').val(parseFloat(this.mapRadius()));
        }
    },

    mapRadius: function() {
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
