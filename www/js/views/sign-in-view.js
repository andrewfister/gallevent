var SignInView = Backbone.View.extend({
    className: 'sign-in-status',
    
    events: {
        'click .btn-sign-in': 'signIn',
        'click #signIn': 'showSignIn',
        'click .btn-sign-out': 'signOut'
    },
    
    render: function() {
    },
    
    renderSignedIn: function() {
        this.el.empty();
        this.el.append("<a href='" + this.model.urlRoot + "'>" + this.model.username + "</a><a class='.btn-sign-out'>Sign Out</a></span>");
    },
    
    renderSignedOut: function() {
    },
    
    showSignIn: function() {
        $(".sign-in-form").slideToggle(600);
    },
    
    signIn: function() {
        this.model.signIn(this.renderSignedIn);
    },
    
    signOut: function() {
        this.model.signOut(this.renderSignedOut);
    }
});
