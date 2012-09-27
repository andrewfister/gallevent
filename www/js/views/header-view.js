var HeaderView = Backbone.View.extend({
    id: "front-page",
    render: function() {
        $( "#date1" ).datepicker({ dateFormat: "mm/dd/yyyy" });
	    $( "#date2" ).datepicker({ dateFormat: "mm/dd/yyyy" });
	    $( "#start-date" ).datepicker({ dateFormat: "mm/dd/yy" });
	    $( "#end-date" ).datepicker({ dateFormat: "mm/dd/yy" });
    }
});
