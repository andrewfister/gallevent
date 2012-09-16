var FrontPageView = Backbone.View.extend({
    id: "front-page",
    render: function() {
        
    }
});

$(function(){  // on page load
    mapEvents.url = "/event/events/?userId=" + $('#user-id').html();
    
    var event = new Event({category: });
    var frontPageView = new FrontPageView({
        id: 'front-page',
        model: event,
    });
    frontPageView.render();
});
