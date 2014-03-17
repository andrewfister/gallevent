var PostEventView = Backbone.View.extend({
    id: "post-event",

    initialize: function() {
        // Hide and show the guest list/ ticket sections
        // if the corresponding button is pushed
        $('.opt-tickets').hide();
        $('.opt-guest-l').hide();
        $('.btn-tickets').removeClass('active');
        $('.btn-guest-l').removeClass('active');


        $(".btn-guest-l").click(function() {
        
            $('.opt-guest-l').show();
            $('.btn-guest-l').addClass("active");

            $('.opt-tickets').hide();
            $('.btn-tickets').removeClass("active");

        });

        $(".btn-tickets").click(function() {
        
            $('.opt-guest-l').hide();
            $('.btn-guest-l').removeClass("active");

            $('.opt-tickets').show();
            $('.btn-tickets').addClass("active");

        });
        
        this.render();
    },

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
        };
        
        var eventCategory = $("#event-category").attr("repost");
        if ($("#select-" + eventCategory)) {
            $("#select-" + eventCategory).attr("selected", "selected");
        };
        
        //this.setLocationOnMap();
        
        //Geocode address entered in the form when there's an address change 
        //and there's enough address information
        /*
        $(".location").blur(function() {
            this.setLocationOnMap();
        }.bind(this));
        */

       addressParse =  this.addressParse;

        $( "#address" ).blur(function() {
            var addressComponents= {  };
            addressParse( this.value,  addressComponents ) ;           

        });

        return this;
    },

    
    setLocationOnMap: function() {
        var address = $("#address").attr("value");
    
        if (address.length > 0)
        {
            this.codeAddress(address);
            this.model.on('pinDropped', function() {
            this.model.trigger('open');
            }, this);

        }
    },
    


    addressParse : function(locationAddress, addressComponents) {
            var geocoder = new google.maps.Geocoder();

            geocoder.geocode({ address: locationAddress }, function(results, status) {

            if (status === google.maps.GeocoderStatus.OK) { 
                // decoding OK
                var newLocation = results[0].address_components;
                var geom = results[0].geometry.location;
                addressComponents["longitude"] =  geom.lng();
                addressComponents["latitude"] =  geom.lat();

                for(var i=0; i<newLocation.length; i++) 
                 {
                   var component_type = newLocation[i]["types"][0];
                   var component_value = newLocation[i]["short_name"];

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
                        }  // switch
                }    // for 

                $("#latitude").val( addressComponents["latitude"]); 
                $("#longitude").val( addressComponents["longitude"]);
                $("#street_number").val( addressComponents["street_number"]);
                $("#street").val(addressComponents["street"]);
                $("#city").val(addressComponents["city"]);
                $("#state").val( addressComponents["state"]);
                $("#zipcode").val( addressComponents["zipcode"]);


            }
            else { 
                alert('Please enter valid address.');
              }
          }.bind(this) );
  
        return event;  
    },  // function()
                

    codeAddress: function(address) {
        var geocoder = new google.maps.Geocoder();
        
        geocoder.geocode( { 'address': address}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                var location = results[0].geometry.location;
                this.model.set({latitude: location.lat(), longitude: location.lng()});
                $("#latitude").attr("value", location.lat());
                $("#longitude").attr("value", location.lng());
                $("#address").attr("value", results[0].formatted_address);
                
                var addressComponents = results[0].address_components;
                for (var i = 0; i < addressComponents.length; i++)
                {
                    var addressComponent = addressComponents[i];
                    var componentName = addressComponent.long_name;
                    var componentTypes = addressComponent.types;
                    
                    for (var j = 0; j < componentTypes.length; j++)
                    {
                        var componentType = componentTypes[j];
                        var addressComponentElementId = "";
                        switch (componentType)
                        {
                            case 'street_number':
                                addressComponentElementId = "street_number";
                            break;
                            case 'route':
                                addressComponentElementId = "street";
                            break;
                            case 'subpremise':
                                addressComponentElementId = "subpremise";
                            break;
                            case 'locality':
                                addressComponentElementId = "city";
                            break;
                            case 'administrative_area_level_1':
                                addressComponentElementId = "state";
                                componentName = addressComponent.short_name;
                            break;
                            case 'postal_code':
                                addressComponentElementId = "zipcode";
                            break;
                        }
                        
                        if (addressComponentElementId.length > 0)
                        {
                            $('#' + addressComponentElementId).attr("value", componentName);
                        }
                    }
                }
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
