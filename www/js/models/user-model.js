var User = Backbone.Model.extend({
    defaults: {
        'id': 0,
        'username': '',
        'first_name': '',
        'last_name': '',
        'email': '',
    },
    
    urlRoot: '/profile/user',
});
