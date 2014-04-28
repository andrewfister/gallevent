// on dom load
$(document).ready(function() {
    window.dispatcher = _.clone(Backbone.Events);
    
    window.userProfileView = new UserProfileView();
});
