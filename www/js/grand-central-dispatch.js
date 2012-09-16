// on dom load
$(function() {
    var views = [];
    var events = new EventCollection;
    
    if ($('#map_canvas'))
    {
        events.reset(eventsJSON);
        
        var mapView = new MapView({
            collection: events
        });
        mapView.render();
    }
});
