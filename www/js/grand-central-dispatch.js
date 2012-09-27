// on dom load
$(function() {
    var events = new EventCollection;
    events.reset(eventsJSON);
    
    if ($('#pin-key').length)
    {
        var categories = ['networking', 'education', 'fairs', 'athletic', 'art', 'dancing', 'dining', 'parties'];
        $('.key').click(function() {
            _.each(categories, function(item, index, items) {
                $('.'+item).click(function() {
                    events.reset(eventsJSON);
                    events.reset(events.where({category: item}));
                });
            });
        });
    }
    
    if ($('#your-posts').length)
    {
        console.log("SEE THIS SHIT COME UP");
        var archivedEvents = new EventCollection(events.where({status: 2}));
        events.reset(events.where({status: 1}));
    
        events.on('change:status', function(evt, index, options) {
            var archiveEvent = evt.collection.get(evt.id);
            this.remove(archiveEvent);
            archivedEvents.add(archiveEvent);
        }, events);
    
        _.each(events.models, function(item, index, items) {
            var yourPostView = new YourPostView({
                model: item,
                id: 'your-post-' + item.id,
            });
            yourPostView.render();
        });
        
        archivedEvents.on('change:status', function(evt, index, options) {
            var deleteEvent = evt.collection.get(evt.id);
            this.remove(deleteEvent);
        }, archivedEvents);
        
        archivedEvents.on('add', function(evt, collection, options) {
            var yourArchivedPostView = new YourArchivedPostView({
                model: collection.models[options.index],
                el: $('.archived-events'),
            });
            yourArchivedPostView.render();
        }, archivedEvents);
        
        _.each(archivedEvents.models, function(item, index, items) {
            var yourArchivedPostView = new YourArchivedPostView({
                model: item,
                id: 'your-post-' + item.id,
            });
            yourArchivedPostView.render();
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
    
    if ($('#map_canvas').length)
    {   
        var mapView = new MapView({
            collection: events
        });
        mapView.render();
    }
    
    if ($('#header').length)
    {
        var headerView = new HeaderView({
        });
        headerView.render();
    }
});
