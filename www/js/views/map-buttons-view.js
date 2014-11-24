var MapButtonsView = Backbone.View.extend({
    events: {
        'click .btn-filters': 'showFilters'
    },

    initialize: function() {

    },

    showFilters: function() {
        $('#filters').toggleClass('hidden');
    }
});