var PinKeyView = Backbone.View.extend({
    id: 'pin-key',
    
    categories: ['networking', 'education', 'fairs', 'athletic', 'art', 'dancing', 'dining', 'nightlife'],
    
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
        
        this.collection.on('reset', this.updatePinKeys.bind(this));
    },
    
    updatePinKeys: function() {
        $('.key').removeClass('disabled');
        
        _.each(this.categories, function(category, index, categories) {
            var categoryCount = window.events.categoryCounts[category];
        
            if (categoryCount === 0) {
                this.pinKeys[category].addClass('disabled');
                $('.' + category + ' .category-count').addClass("hidden");
            }
            else {
                $('.' + category + ' .category-count').text(categoryCount)
                                                    .removeClass("hidden");
            }
        }, this);
    },
    
    requestPinKeys: function() {
        _.each(this.categories, function(category, index, categories) {
            $('.' + category + ' .category-count').addClass("hidden");
        }, this);
    }
});
