// on dom load
$(function() {
    var events = new EventCollection();
    
	if (typeof eventsJSON !== 'undefined')
	{
        events.reset(eventsJSON);
	}
	
	if ($('.sign-in-status').length)
	{
	    var userView = new UserView({});
	    userView.render();
	}
    
    if ($('#pin-key').length)
    {
        var categories = ['networking', 'education', 'fairs', 'athletic', 'art', 'dancing', 'dining', 'parties'];
        
        _.each(categories, function(item, index, items) {
            $('.'+item).click(function() {
                $('.key').removeClass('active');
                
                if ($('.'+item).hasClass('inactive') || !$('.key').hasClass('inactive'))
                {
                    mapView.collection.reset(events.where({category: item}));
                    $('.key').addClass('inactive');
                    $('.'+item).removeClass('inactive');
                    $('.'+item).addClass('active');
                }
                else
                {
                    $('.key').removeClass('inactive');
                }
            });
        });
    }
    
/*    if ($('#your-posts').length)
    {
        var archivedEvents = new EventCollection(events.where({status: 2}));
        var yourActivePostsView = new YourActivePostsView({collection : events});
        yourActivePostsView.render();
        //events.reset(eventsJSON);  
        var yourArchivedPostsView = new YourArchivedPostsView({collection : archivedEvents});
        yourArchivedPostsView.render();
    }

    if ($('#your-posts').length)
    {  
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
        
        postEventView.model.on("change:longitude", function() {
            events.reset([this]);
        });
        
        postEventView.render();
    }*/
    
    if ($('#map_canvas').length)
    {
        var mapEvents = new EventCollection();
        events.on('reset', function() { 
            mapEvents.reset(events.models);
        });
        
        var mapView = new MapView({
            collection: mapEvents
        });
        mapView.render();
    }
    
    /*if ($('#header').length)
    {
        var headerView = new HeaderView({
        });
        headerView.render();
    }*/
    
    if ($('#top-search').length)
    {
        var searchView = new SearchView({
            collection: events
        });
        searchView.render();
    }
});
