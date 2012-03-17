/*-------------- START INFO WINDOW HTML ---------*/

var contentString = '<div class="map-popup">'+
	'<div class="event-name cb-networking"><a href="#">2nd Annual Bay Area Brew Festival</a></div>'+
    '<div class="price">Price: $50</div>'+
	'<div class="date-time">Saturday, March 3, 1:00 pm to 5:00 pm</div>'+
	'<div class="description">The 2nd Annual Bay Area Brew Festival follows promises to be even bigger and better... <a href="#">More &raquo;</a></div>'+
	'<div class="address">Marina Blvd, San Francisco, CA 94123</div>'+
	'<div class="btns"><span class="btn-rsvp"><span>RSVP</span></span><span class="btn-track"><span>Track</span></span></div>'+
	'<div class="mod-event"><a href="#">Is this your event?</a><a href="#" class="warning">Report this event</a></div>'+
    '</div>';

/*---------------------- END INFO WINDOW HTML -------------*/



var map;
var geocoder;
var autocomplete;

var last_marker = null;
  
    
function initialize() {
         geocoder = new google.maps.Geocoder();
         
         var myOptions = {
          center: new google.maps.LatLng(37.88397, -122.2644), 
          zoom: 8,
          mapTypeId: google.maps.MapTypeId.ROADMAP
        }; 
 
        map = new google.maps.Map(document.getElementById("map_canvas"),
            myOptions);


	var input = document.getElementById("event");
	if (input==null) alert('error');
	var defaultBounds = new google.maps.LatLngBounds(
  			new google.maps.LatLng(36.8902, -123.1759),
  			new google.maps.LatLng(39.8474, -121.2631));

	var autoopts = {
  		bounds: defaultBounds,
  		types: ['establishment']
	};

	autocomplete = new google.maps.places.Autocomplete(input, autoopts);
}    
	  

function codeAddress(txt_event) {
   
var address = txt_event.value;

var image = '/static/img/pin-map-dining.png';

var infowindow = new google.maps.InfoWindow({
    content: contentString
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
  }
	 
google.maps.event.addDomListener(window, 'load', initialize);
