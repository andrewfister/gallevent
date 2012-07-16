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
		    $(elem).siblings(".formOptionalToggle").change(function(event) {
			    var content = $(event.target).siblings(".formOptional");
			    if (visible) {
				    content.slideUp();
			    } else {
				    content.slideDown();
			    }
			    visible = !visible;
		    });
	    });
        
        $(".location").blur(function() {
            var address1 = $("#address1").attr("value");
            var city = $("#city").attr("value");
            var zipcode = $("#zipcode").attr("value");
            
            var address = address1 + ', ' + city + ' ' + zipcode;
            var location = this.codeAddress(address, {
                address1: address1,
                city: city,
                zipcode: zipcode,
            });
        }.bind(this));
        
        return this;
    },
    
    codeAddress: function(address, event) {
        var geocoder = new google.maps.Geocoder();
            
        geocoder.geocode( { 'address': address}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                var location = results[0].geometry.location;
                event.latitude = location.lat();
                event.longitude = location.lng();
                mapEvents.reset([event]);
            } else {
                alert("Geocode was not successful for the following reason: " + status); 
            }
        });
    },
});
