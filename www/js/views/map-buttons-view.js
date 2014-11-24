var MapButtonsView = Backbone.View.extend({
    events: {
        'click .btn-filters': 'showFilters',
        'click .btn-list': 'showList'
    },

    initialize: function() {

    },

    showFilters: function() {
        $('#filters').toggleClass('hidden');
    },

    showList: function() {
        $('#event-list').toggleClass('active');
    }
});