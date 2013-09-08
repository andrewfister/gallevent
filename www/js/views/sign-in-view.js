var SignInView = Backbone.View.extend({
    className: 'sign-in-status',
    
    events: {
        'click .btn-sign-in': 'signIn',
        'click .btn-sign-out': 'signOut',
        'click #btn-show-sign-in': 'showSignIn',
        'click #btn-show-join': 'showJoin',
        'click .alt-sign-in': 'switchForm',
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
        this.showJoinForm = true;
        this.switchForm();
        
        $(".sign-in-form").slideToggle(600, function() {
		    $(".signed-out").toggleClass('active');
		});
    },
    
    showJoin: function() {
        this.showJoinForm = false;
        this.switchForm();
        
        $(".sign-in-form").slideToggle(600, function() {
			$(".signed-out").toggleClass('active');
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
    
    signOut: function() {
        this.model.signOut(this.renderSignedOut.bind(this), this.render);
        this.model.clear();
    }
});
