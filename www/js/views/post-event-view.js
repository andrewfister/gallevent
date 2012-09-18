var PostEventView = Backbone.View.extend({
    id: "post-event",
    render: function() {
        //START Limit characters in textarea 
        //http://www.devcurry.com/2009/08/limit-number-of-characters-in-textarea.html
        $('#event-description').keyup(function() {
            var len = this.value.length;
            $('#charLeft').text(1000 - len);
        });
    
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
        
        //Default selected option for dropdowns
        var eventState = $("#state").attr("repost");
        if ($("#state > [value=" + eventState + "]")) {
            $("#state > [value=" + eventState + "]").attr("selected", "selected");
        }
        
        var eventCategory = $("#event-category").attr("repost");
        if ($("#select-" + eventCategory)) {
            $("#select-" + eventCategory).attr("selected", "selected");
        }
        
        this.setLocationOnMap();
        
        //Geocode address entered in the form when there's an address change 
        //and there's enough address information
        $(".location").blur(function() {
            this.setLocationOnMap();
        }.bind(this));
        
        return this;
    },
    
    setLocationOnMap: function() {
        var address1 = $("#address1").attr("value");
        var address2 = $("#address2").attr("value");
        var city = $("#city").attr("value");
        var zipcode = $("#zip-code").attr("value");
        
        if (address1.length > 0 && city.length > 0 && zipcode.length > 0)
        {
            this.model.set({
                address1: address1,
                address2: address2,
                city: city,
                zipcode: zipcode,
            });
        
            var address = this.model.getAddress();
            this.codeAddress(address);
        }
    },
    
    codeAddress: function(address) {
        var geocoder = new google.maps.Geocoder();
        
        geocoder.geocode( { 'address': address}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                var location = results[0].geometry.location;
                this.model.set({latitude: location.lat(), longitude: location.lng()});
                $("#latitude").attr("value", location.lat());
                $("#longitude").attr("value", location.lng());
            } else {
                alert("Geocode was not successful for the following reason: " + status); 
            }
        }.bind(this));
        
        return event;
    },
    
    redirectToYourPosts: function() {
        window.location = "/event/show";
    }
});
