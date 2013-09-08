var SignInView = Backbone.View.extend({
    className: 'sign-in-status',
    
    events: {
        'click .btn-sign-in': 'signIn',
        'click .btn-sign-out': 'signOut',
        'click #btn-show-sign-in': 'showSignIn',
        'click #btn-show-join': 'showJoin'
    },
    
    render: function() {
    },
    
    renderSignedIn: function(response, success, request) {
        if (response.success) {
            this.model.set(response.user);
            $('.username').text(this.model.get('userName'));
            $('.signed-out').addClass('hidden');
            $('.signed-in').removeClass('hidden');
            $('.sign-in-message').text('');
        }
        else {
            $('.sign-in-message').text('Incorrect email or password');
        }
    },
    
    renderSignedOut: function() {
        $('.username').text("");
        $('.signed-in').addClass('hidden');
        $('.signed-out').removeClass('hidden');
    },
    
    showSignIn: function() {
        /*$(".sign-in-form").slideToggle(600, function() {
			
		});*/
		$(".signed-out").toggleClass('active');
		
        $(".btn-sign-in").text('Sign In')
                        .click(this.signIn.bind(this));
        $(".sign-in-form").removeClass('join-form');
    },
    
    showJoin: function() {
        /*$(".sign-in-form").slideToggle(600, function() {
			
		});*/
		$(".signed-out").toggleClass('active');
        $(".btn-sign-in").text('Join')
                        .click(this.signIn.bind(this));
        $(".sign-in-form").addClass('join-form');
    },
    
    signIn: function() {
        var callJoin = false;
        if ($(".sign-in-form").hasClass("join-form")) {
            callJoin = true;
        }
        
        this.model.signIn(this.renderSignedIn.bind(this), this.render, callJoin);
    },
    
    signOut: function() {
        this.model.signOut(this.renderSignedOut.bind(this), this.render);
        this.model.clear();
    }
});
