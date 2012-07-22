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
        
        $(".location").blur(function() {
            var address1 = $("#address1").attr("value");
            var address2 = $("#address2").attr("value");
            var city = $("#city").attr("value");
            var zipcode = $("#zip-code").attr("value");
            
            if (address1.length > 0 && city.length > 0 && zipcode.length > 0)
            {
                var event = new Event({
                    address1: address1,
                    address2: address2,
                    city: city,
                    zipcode: zipcode,
                });
            
                var address = event.getAddress();
                this.codeAddress(address, event);
            }
        }.bind(this));
        
        return this;
    },
    
    codeAddress: function(address, event) {
        var geocoder = new google.maps.Geocoder();
            
        geocoder.geocode( { 'address': address}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                var location = results[0].geometry.location;
                event.set({latitude: location.lat(), longitude: location.lng()});
                mapEvents.reset([event]);
            } else {
                alert("Geocode was not successful for the following reason: " + status); 
            }
        });
    },
});
