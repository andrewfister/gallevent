var User = Backbone.Model.extend({
    defaults: {
        'id': 0,
        'userName': '',
        'firstName': '',
        'lastName': '',
        'email': '',
        'latitude': 0,
        'longitude': 0
    },
    
    signIn: function(success, failure=null) {
        var serializedSignIn = $('.sign-in-form').serializeArray();
        
        var signInParams = {};
        var i;
        for (i = 0; i < serializedSignIn.length; i++)
        {
            signInParams[serializedSignIn[i].name] = serializedSignIn[i].value;
        }
    
        $.ajax(this.signInUrl, {
            type: 'POST',
            data: signInParams,
            success: success,
            failure: failure
        });
    },
    
    signOut: function(success, failure=null) {
        $.ajax(this.signOutUrl, {
            type: 'POST',
            success: success,
            failure: failure
        });
    },
    
    signInUrl: '/login/sign_in/',
    signOutUrl: '/login/sign_out/',
    urlRoot: '/profile/user/'
});
