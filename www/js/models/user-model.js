var User = Backbone.Model.extend({
    defaults: {
        'id': 0,
        'username': 'example@domain.com',
        'first_name': '',
        'last_name': '',
        'email': 'example@domain.com',
    },
    
    url: '/profile/user',
});
