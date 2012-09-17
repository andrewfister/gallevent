// on dom load
$(function() {
    var events = new EventCollection;
    events.reset(eventsJSON);
    
    if ($('#map_canvas').length)
    {   
        var mapView = new MapView({
            collection: events
        });
        mapView.render();
    }
    
    if ($('#your-posts').length)
    {
        events.on('change:status', function(evt, index, options) {
            this.remove(this.models[index]);
        }, events);
    
        _.each(events.models, function(item, index, items) {
            var yourPostView = new YourPostView({
                model: item,
                id: 'your-post-' + item.id,
                el: $('#your-post-' + item.id),
            });
            yourPostView.render();
        });
    }
    
    if ($('#post-event').length)
    {
        var event = new Event();
        var postEventView = new PostEventView({
            model: event,
        });
        postEventView.render();
    }
});
