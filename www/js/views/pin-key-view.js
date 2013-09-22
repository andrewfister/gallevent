var PinKeyView = new Backbone.View.extend({
    id: 'pin-key',
    
    initialize: function() {
        _.each(this.categories, function(item, index, items) {
            $('.'+item).click(function() {
                $('.key').removeClass('active');
                
                if (window.events.categoryCounts[item] > 0
                    && ($('.'+item).hasClass('inactive') 
                    || !$('.key').hasClass('inactive')))
                {
                    this.collection.reset(window.events.where({category: item}));
                    $('.key').addClass('inactive');
                    $('.'+item).removeClass('inactive').addClass('active');
                }
                else
                {
                    $('.key').removeClass('inactive');
                }
            }.bind(this));
        }, this);
    }
});
