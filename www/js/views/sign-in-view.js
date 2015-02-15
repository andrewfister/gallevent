var SignInView = Backbone.View.extend({
    className: 'sign-in-status',
    
    events: {
        'click .btn-sign-in': 'signIn',
        'click .btn-sign-out': 'signOut',
        'click .sign-in-cta': 'showSignIn',
    },
    
    initialize: function() {
        $('.sign-in-form').keypress(function(event) {
            if (event.which === 13) {
                this.signIn();
            }
        }.bind(this));

        window.dispatcher.on('click', function(event) {
            if (this !== event.target &&
               !$('.sign-in-status').has(event.target).length &&
               !$(event.target).is('.sign-in-status')) {
                   $('.sign-in-ui').removeClass('active');
               }
        });
        
        this.render();
    },
    
    render: function() {
    },
    
    renderSignedIn: function(response, success, request) {
        if (response.success) {
            this.model.set(response.user);

            $('.signed-out').fadeOut(600, function() {
                $('.sign-in-ui').removeClass('active');
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
        $(".sign-in-ui").toggleClass("active");
    },

    signIn: function() {
        this.model.signIn(this.renderSignedIn.bind(this), this.render, false);
    }
});
