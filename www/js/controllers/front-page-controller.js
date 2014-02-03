// on dom load
$(document).ready(function() {
    window.events = new EventSearchCollection();

    window.searchView = new SearchView({
        collection: window.events
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
});
