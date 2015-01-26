var SignInView = Backbone.View.extend({
    className: 'sign-in-status',
    
    events: {
        'click .btn-sign-in': 'signIn',
        'click .btn-sign-out': 'signOut',
    },
    
    initialize: function() {
        this.showJoinForm = false;
        
        $('.sign-in-form').keypress(function(event) {
            if (event.which === 13) {
                this.signIn();
            }
        }.bind(this));

        $('.sign-in-ui').click(function(event) {
            $('.sign-in-ui').toggleClass('active');
        });
        
        this.render();
    },
    
    render: function() {
    },
    
    renderSignedIn: function(response, success, request) {
        if (response.success) {
            this.model.set(response.user);

            $('.signed-out').fadeOut(600, function() {
                $('.signed-out').addClass('hidden');
                $('.username').text(this.model.get('userName'));
                $('.sign-in-message').text('');

                $('.signed-in').fadeIn(600, function() {
                    $('.signed-in').removeClass('hidden');
                }.bind(this));
            }.bind(this));
        } else {
            $('.sign-in-message').text("Username or password is incorrect!");
        }
    },
    
    renderSignedOut: function() {
        $('.signed-in').fadeOut(600, function() {
            $('.username').text("");
            $('.signed-in').addClass('hidden');
        });
        
        $('.signed-out').fadeIn(600, function() {
            $('.signed-out').removeClass('hidden');
        });
    },
    
    showSignIn: function() {
        this.switchForm();
        
        $(".sign-in-form").removeClass("hidden", function() {
	        $(".signed-out").toggleClass('active');
	        $(".sign-in-form").removeClass("invisible");
        });
    },
    
    signIn: function() {
        this.model.signIn(this.renderSignedIn.bind(this), this.render, false);
    }
});
