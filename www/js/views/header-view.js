var HeaderView = Backbone.View.extend({
    id: "front-page",
    render: function() {
        $( "#date1" ).datepicker();
	    $( "#date2" ).datepicker();
	    $( "#start-date" ).datepicker();
	    $( "#end-date" ).datepicker();
    }
});
