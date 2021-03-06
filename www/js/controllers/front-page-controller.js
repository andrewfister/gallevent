// on dom load
$(document).ready(function() {
    window.dispatcher = _.clone(Backbone.Events);
    window.events = new EventSearchCollection();

    if ($('.sign-in-status').length) {
        $(document).on('click', function(event) {
            window.dispatcher.trigger('click', event);
        });

        window.signInUser = new User();
        window.signInView = new SignInView({
            el: $('.sign-in-status'),
            model: window.signInUser
        });
        window.signInView.render();
    }

    window.searchView = new SearchView({
        collection: window.events,
        el: $('#filters')
    });

    window.mapEvents = new EventCollection();
    window.events.on('reset', function() {
        window.mapEvents.reset(window.events.models);
    });

    window.mapView = new MapView({
        collection: window.mapEvents
    });

    window.pinKeyView = new PinKeyView({
        collection: window.mapEvents
    });

    window.mapButtonsView = new MapButtonsView({
        el: $('.map-btns')
    });
    
    window.eventListView = new EventListView({
        collection: window.mapEvents,
        el: $('#event-list')
    });
});
