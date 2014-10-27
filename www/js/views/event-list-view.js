var EventListView = Backbone.View.extend({
    initialize: function() {
        this.eventListItemTemplate = Mustache.template('event-list-item').render;
    
        this.collection.on('reset', this.render.bind(this));
        this.render();
    },
    
    render: function() {
        this.$el.empty();
        _.each(this.collection.models, function(event, index, events) {
            this.$el.append(Mustache.template('event-list-item').render(event.toJSON()));
        }.bind(this));
    },
});
