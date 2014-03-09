// on dom load
$(document).ready(function() {
    window.dispatcher = _.clone(Backbone.Events);
    window.events = new Event(window.eventJSON);

    window.signInUser = new User();
    window.signInView = new SignInView({
        el: $('.sign-in-status'),
        model: window.signInUser
    });

    window.mapEvents = new EventCollection();
    window.events.on('reset', function() {
        window.mapEvents.reset(window.events.models);
    });

    window.mapView = new MapView({
        collection: window.mapEvents
    });
    
    window.postEventView = new PostEventView({
        el: $('#post-event-form'),
        model: window.event
    });
});
