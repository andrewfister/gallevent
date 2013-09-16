var SignInView = Backbone.View.extend({
    className: 'sign-in-status',
    
    events: {
        'click .btn-sign-in': 'signIn',
        'click .btn-sign-out': 'signOut',
        'click #btn-show-sign-in': 'showJoinOrSignIn',
        'click #btn-show-join': 'showJoinOrSignIn',
        'click .alt-sign-in': 'switchFormToAlt',
    },
    
    initialize: function() {
        this.showJoinForm = true;
    },
    
    render: function() {
    },
    
    renderSignedIn: function(response, success, request) {
        if (response.success) {
            if (this.showJoinForm) {
                location.href = "/profile/show";
            }
        
            this.model.set(response.user);
            
            $('.signed-out').fadeOut(600, function() {
                $('.signed-out').addClass('hidden');
            });
            
            $('.signed-in').fadeIn(600, function() {
                $('.username').text(this.model.get('userName'));
                $('.sign-in-message').text('');
                $('.signed-in').removeClass('hidden');
            });
        }
        else {
            $('.sign-in-message').text('Incorrect email or password');
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
    
    showJoinOrSignIn: function(event) {
        $("#btn-show-join").fadeOut(600);
        
        $("#btn-show-sign-in").fadeOut(600, function() {
            if (event.target.id == "btn-show-sign-in") {
                this.showSignIn();
            }
            else {
                this.showJoin();
            }
        }.bind(this));
    },
    
    showSignIn: function() {
        this.showJoinForm = true;
        this.switchForm();
        
        $(".sign-in-form").removeClass("hidden", function() {
	        $(".signed-out").toggleClass('active');
	        $(".sign-in-form").removeClass("invisible");
        });
    },
    
    showJoin: function() {
        this.showJoinForm = false;
        this.switchForm();
        
        $(".sign-in-form").removeClass("hidden", function() {
	        $(".signed-out").toggleClass('active');
	        $(".sign-in-form").removeClass("invisible");
        });
    },
    
    signIn: function() {
        this.model.signIn(this.renderSignedIn.bind(this), this.render, this.showJoinForm);
    },
    
    switchForm: function() {
        if (this.showJoinForm) {
            $(".btn-sign-in").text('Sign In');
            $(".alt-sign-in").text('Join');
            this.showJoinForm = false;
        }
        else {
            $(".btn-sign-in").text('Join');
            $(".alt-sign-in").text('Sign In');
            this.showJoinForm = true;
        }
    },
    
    switchFormToAlt: function() {
        $(".sign-in-form").fadeOut(600, function() {
            this.switchForm();
            $(".sign-in-form").fadeIn(600);
        }.bind(this));
    },
    
    signOut: function() {
        this.model.signOut(this.renderSignedOut.bind(this), this.render);
        this.model.clear();
    }
});
