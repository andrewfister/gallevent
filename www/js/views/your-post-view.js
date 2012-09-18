var YourPostView = Backbone.View.extend({
    template: function(attributes) 
    {
        attributes['btn-class'] = "btn-archive";
        attributes['btn-text'] = "Archive";
        return Mustache.template('your-post').render(attributes);
    },
    
    render: function() {
        $('.active-events').append(this.template(this.model.attributes));
        
        this.el = $('#your-post-' + this.model.id);
        
        $("#btn-archive-" + this.model.id).bind("click", function() {
            this.model.on('change:status', function() {
                $('#your-post-' + this.model.id).remove();
            }, this);
            this.model.save({'status': 2});
        }.bind(this));
        
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
    
    render: function() {
        $('.archived-events').append(this.template(this.model.attributes));
        
        this.el = $('#your-post-' + this.model.id);
        
        $("#btn-delete-" + this.model.id).bind("click", function() {
            this.model.on('change:status', function() {
                $('#your-post-' + this.model.id).remove();
            }, this);
            this.model.save({'status': 0});
        }.bind(this));
        
        return this;
    },
});
