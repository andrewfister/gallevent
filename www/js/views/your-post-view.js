var YourPostView = Backbone.View.extend({
    template: function(attributes) 
    {
        attributes['btn-class'] = "btn-archive";
        attributes['btn-text'] = "Archive";
        attributes['list-status'] = "list-active";
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
        attributes['list-status'] = "list-archived";
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

var YourActivePostsView = Backbone.View.extend({

    initialize: function() {

        $('#active-sort-by1').change(function() {
            $('.list-active').remove();
            var selectedOption = $('#active-sort-by1 option:selected').text();
            if(selectedOption == "Date Ascending")
                this.collection.orderDateAscend();
            else if(selectedOption == "Date Descending")
                this.collection.orderDateDescend();
            else
                this.collection.orderCategory()
            this.render();

        }.bind(this));            
    },

   
    render: function() {
          var archivedEvents = new EventCollection(this.collection.where({status: 2}));
          this.collection.reset(this.collection.where({status: 1}));

        this.collection.on('change:status', function(evt, index, options) {
            var archiveEvent = evt.collection.get(evt.id);
            this.remove(archiveEvent);
            archivedEvents.add(archiveEvent);
        }, this.collection);
    
        _.each(this.collection.models, function(item, index, items) {
            var yourPostView = new YourPostView({
                model: item,
                id: 'your-post-' + item.id
            });
            
            yourPostView.render();
        });
    }

});

var YourArchivedPostsView = Backbone.View.extend({

    initialize: function() {

        $('#active-sort-by3').change(function() {
            $('.list-archived').remove();
            var selectedOption = $('#active-sort-by3 option:selected').text();
            if(selectedOption == "Date Ascending")
                this.collection.orderDateAscend();
            else if(selectedOption == "Date Descending")
                this.collection.orderDateDescend();
            else
                this.collection.orderCategory()
            this.render();

        }.bind(this));            
    },

    render: function() {
        
        this.collection.on('change:status', function(evt, index, options) {
            var deleteEvent = evt.collection.get(evt.id);
            this.remove(deleteEvent);
        }, this.collection);
            
        this.collection.on('add', function(evt, collection, options) {
            var yourArchivedPostView = new YourArchivedPostView({
                model: collection.models[options.index],
                el: $('.archived-events'),
            });
            yourArchivedPostView.render();
        }, this.collection);
            
        _.each(this.collection.models, function(item, index, items) {
            var yourArchivedPostView = new YourArchivedPostView({
                model: item,
                id: 'your-post-' + item.id
            });
            yourArchivedPostView.render();
        });
    }
});

