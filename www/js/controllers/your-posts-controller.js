// on dom load
$(document).ready(function() {
    window.dispatcher = _.clone(Backbone.Events);
    window.events = new EventCollection(window.eventsJSON);
    
    window.yourActivePostsView = new YourActivePostsView({
        collection: window.events,
        el: $('.active-events')
    });
    
    window.yourArchivedPostsView = new YourActivePostsView({
        collection: window.events,
        el: $('.archived-events')
    });
});
