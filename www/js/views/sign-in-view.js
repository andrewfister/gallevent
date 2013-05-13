var SignInView = Backbone.View.extend({
    className: 'sign-in-status',
    
    events: {
        'click .btn-sign-in': 'signIn',
        'click .btn-sign-out': 'signOut',
        'click #signIn': 'showSignIn',
    },
    
    render: function() {
    },
    
    renderSignedIn: function(response, success, request) {
        this.model.set(response.user);
        $('.username').text(this.model.get('userName'));
        $('.signed-out').addClass('hidden');
        $('.signed-in').removeClass('hidden');
    },
    
    renderSignedOut: function() {
        $('.username').text("");
        $('.signed-in').addClass('hidden');
        $('.signed-out').removeClass('hidden');
    },
    
    showSignIn: function() {
        $(".sign-in-form").slideToggle(600);
        $(".btn-sign-in").click(this.signIn.bind(this));
    },
    
    signIn: function() {
        this.model.signIn(this.renderSignedIn.bind(this));
    },
    
    signOut: function() {
        this.model.signOut(this.renderSignedOut.bind(this));
    }
});
