var User = Backbone.Model.extend({
    defaults: {
        'id': 0,
        'username': '',
        'firstName': '',
        'lastName': '',
        'email': '',
        'latitude': 0,
        'longitude': 0
    },
    
    signIn: function(success, failure=null) {
        $.ajax(this.signInUrl, {
            success: success,
            failure: failure
        });
    },
    
    signInUrl: '/login/sign_in',

    urlRoot: '/profile/user'
});
