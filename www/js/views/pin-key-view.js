var PinKeyView = Backbone.View.extend({
    id: 'pin-key',
    
    categories: ['networking', 'education', 'fairs', 'athletic', 'art', 'dancing', 'dining', 'parties'],
    
    initialize: function() {
        this.pinKeys = {};
        this.selectedCategory = "";
        
        _.each(this.categories, function(category, index, categories) {
            this.pinKeys[category] = $('.' + category);
            
            this.pinKeys[category].click(function() {
                if (window.events.categoryCounts[category] > 0) {
                    $('.key').removeClass('selected');
                    
                    if (this.selectedCategory === category) {
                        this.collection.reset(window.events.models);
                        this.selectedCategory = "";
                    }
                    else {
                        this.pinKeys[category].addClass('selected');
                        this.collection.reset(window.events.where({category: category}));
                        this.selectedCategory = category;
                    }
                }
            }.bind(this));
        }, this);
        
        this.collection.on('reset', this.disablePinKeys.bind(this));
    },
    
    disablePinKeys: function() {
        $('.key').removeClass('disabled');
        
        _.each(this.categories, function(category, index, categories) {
            if (window.events.categoryCounts[category] === 0) {
                this.pinKeys[category].addClass('disabled');
            }
        }, this);
    }
});
