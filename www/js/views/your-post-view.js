var YourPostView = Backbone.View.extend({
    template: function(attributes) 
    {
        attributes['btn-class'] = "btn-archive";
        attributes['btn-text'] = "Archive";
        return Mustache.template('your-post').render(attributes);
    },
        
    events: {
        "click .mod-event .btn-archive":    "archive",
    },
    
    archive: function() {
        this.model.on('change:status', function() {
            this.remove();
        }, this);
        this.model.save({'status': 2})
    },
    
    render: function() {
        $(this.el).append(this.template(this.model.attributes));
        return this;
    },
});

var YourArchivedPostView = Backbone.View.extend({
    template: function(attributes) 
    {
        attributes['btn-class'] = "btn-delete";
        attributes['btn-text'] = "Delete";
        return Mustache.template('your-post').render(attributes);
    },
    
    events: {
        "click .mod-event .btn-delete":    "destroy",
    },
    
    destroy: function() {
        this.model.on('change:status', function() {
            this.remove();
        }, this);
        this.model.save({'status': 0})
    },
    
    render: function() {
        $(this.el).append(this.template(this.model.attributes));
        return this;
    },
});
