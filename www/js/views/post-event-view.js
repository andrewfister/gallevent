var PostEventView = Backbone.View.extend({
    id: "post-event",
    render: function() {
        // Watermark all input tags:
	    $("input[type='text']").each(function(index, input) {  // Find each input tag
	        input = $(input);              // each gives you a raw HTML element; wrap it back in input
	        if (input.attr('title')) { // if that element has a watermark attribute
		        input.watermark(input.attr('title')); // Use that attribute as the watermark
		    }
	    });
	
	    // Make formOptional divs expand & collapse:
	    $(".formOptional").hide();
	    $(".formOptional").each(function(index, elem) {
		    var visible = false;
			var origElem = $(elem);
			var name = origElem.attr("visibleWhen");
		    $(".formOptionalToggle[name='" + name + "']").change(function(event) {
			    if (visible) {
				    origElem.slideUp();
			    } else {
				    origElem.slideDown();
			    }
			    visible = !visible;
		    });
	    });
        
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
