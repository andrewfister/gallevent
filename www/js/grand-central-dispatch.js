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
        events.on('destroy', function(evt, collection, options) {
            collection.remove(collection[options.index]);
        });
    
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
