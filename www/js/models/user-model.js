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

    signIn: function(success, failure, callJoin) {
        var serializedSignIn = $('.sign-in-form').serializeArray();

        var signInParams = {};
        var i;
        for (i = 0; i < serializedSignIn.length; i++)
        {
            signInParams[serializedSignIn[i].name] = serializedSignIn[i].value;
        }
        
        var ajaxUrl = this.signInUrl;
        if (callJoin) {
            ajaxUrl = this.joinUrl;
        }

        $.ajax(ajaxUrl, {
            type: 'POST',
            data: signInParams,
            success: success,
            failure: failure
        });
    },

    signOut: function(success, failure) {
        var serializedSignIn = $('.sign-in-form').serializeArray();

        var signInParams = {};
        var i;
        for (i = 0; i < serializedSignIn.length; i++)
        {
            signInParams[serializedSignIn[i].name] = serializedSignIn[i].value;
        }
    
        $.ajax(this.signOutUrl, {
            type: 'POST',
            data: signInParams,
            success: success,
            failure: failure
        });
    },

    signInUrl: '/signin/sign_in/',
    signOutUrl: '/signin/sign_out/',
    joinUrl: '/signin/join/',
    urlRoot: '/profile/user/'
});
