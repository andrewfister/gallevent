var MapView = Backbone.View.extend({
    id: "map-canvas",
    
    template: Mustache.template('map').render,
    
    render: function() {
        google.maps.event.addDomListener(window, 'load', function() {
            var map;
            var geocoder;
            
            geocoder = new google.maps.Geocoder();

            var myOptions = {
                center: new google.maps.LatLng(37.88397, -122.2644), 
                zoom: 8,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            }; 

            map = new google.maps.Map($("#map_canvas").get(0),
                myOptions);


            /*var input = document.getElementById("event");
            if (input==null) alert('error');
            var defaultBounds = new google.maps.LatLngBounds(
		            new google.maps.LatLng(36.8902, -123.1759),
		            new google.maps.LatLng(39.8474, -121.2631));

            var autoopts = {
	            bounds: defaultBounds,
	            types: ['establishment']
            };*/
            google.maps.event.addListener(map, 'tilesloaded', function() {
                _.each(this.collection.models, function(item, index, items) {
                    var address = item.attributes.address1 + ' ' + item.attributes.address2 + ', ' + item.attributes.city + ' ' + item.attributes.zipcode;
                    this.codeAddress(address, this.template(item.toJSON()), map, geocoder);
                }, this);
            }.bind(this));
        }.bind(this));
        
        return this;
    },
    
    codeAddress: function(address, infoWindow, map, geocoder) {

        var image = '/static/img/pin-map-dining.png';

        var infowindow = new google.maps.InfoWindow({
            content: infoWindow
        });

        geocoder.geocode( { 'address': address}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                map.setCenter(results[0].geometry.location);
                var marker = new google.maps.Marker({
                    map: map,
                    draggable:true,
                    position: results[0].geometry.location,
                    icon: image,
                    title : address,
                    animation: google.maps.Animation.DROP
                });

            /*	google.maps.event.addListener(marker, 'click', function(){

            if (marker.getAnimation() != null) {
                marker.setAnimation(null);
              } else {
                marker.setAnimation(google.maps.Animation.BOUNCE);
              }

            }); */

            google.maps.event.addListener(marker, 'click', function() {
                infowindow.close();  
                infowindow.open(map,marker);
                last_marker = marker;
            });

            } else {
                alert("Geocode was not successful for the following reason: " + status); 
            }
        });
    },
});
