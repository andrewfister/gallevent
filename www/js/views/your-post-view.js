var YourPostView = Backbone.View.extend({
    className: 'list-post',
        
    events: {
        "click .mod-event .btn-delete":    "destroy",
    },
    
    destroy: function() {
        this.model.on('change:status', function() {
            this.remove();
        }, this);
        this.model.save({'status': 0})
    },
});
