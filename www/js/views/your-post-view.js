var YourPostView = Backbone.View.extend({
    className: 'list-post',
        
    events: {
        "click .mod-event .btn-delete":    "destroy",
    },
    
    destroy: function() {
        this.model.destroy();
        this.remove();
    },
});
