// on dom load
$(document).ready(function() {
    window.events = new EventSearchCollection();

    if (typeof eventsJSON !== 'undefined') {
        window.events.reset(eventsJSON);
    }

    if ($('.sign-in-status').length) {
        window.signInUser = new User();
        window.signInView = new SignInView({
            el: $('.sign-in-status'),
            model: window.signInUser
        });
        window.signInView.render();
    }

    if ($('#map_canvas').length) {
        window.mapEvents = new EventCollection();
        window.events.on('reset', function() {
            window.mapEvents.reset(window.events.models);
        });

        window.mapView = new MapView({
            collection: window.mapEvents
        });
        window.mapView.render();

        if ($('#pin-key').length) {
            window.pinKeyView = new PinKeyView({
                collection: window.mapEvents
            });
            window.pinKeyView.render();
        }
    }

    if ($('#top-search').length) {
        window.searchView = new SearchView({
            collection: window.events
        });
        window.searchView.render();
    }
});
