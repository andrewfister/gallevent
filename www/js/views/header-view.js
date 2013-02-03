var HeaderView = Backbone.View.extend({
    id: "front-page",
    render: function() {
        $( "#date1" ).datepicker({ dateFormat: "mm/dd/yyyy", onSelect: this.changeDate });
        $("#time-span").change(this.changeDate);
		$("#header").slideToggle(600);
		
		if ($("#date1").attr('value').length == 0)
		{
		    var today = new Date();
		    var dd = ('0'+(today.getDate())).slice(-2);
		    var mm = ('0'+(today.getMonth()+1)).slice(-2);
		    var yyyy = today.getFullYear();
		    var formatToday = mm + '/' + dd + '/' + yyyy;
		    $("#date1").attr('value', formatToday);
		}
		
		if ($("#date2").attr('value').length == 0)
		{
		    $("#date2").attr('value', $( "#date1" ).attr('value'));
		}
    },
    
    changeDate: function() {
        if ($("time-span").attr('value') == "day_of")
        {
            $("#date2").attr('value', $( "#date1" ).attr('value'));
        }
        else if ($("time-span").attr('value') == "week_of")
        {
            var date = new Date($( "#date1" ).attr('value'));
            var dayOfWeek = (date.getDay() + 1) % 7;
            
        }
        else if ($("time-span").attr('value') == "weekend_of")
        {
            var date = new Date($( "#date1" ).attr('value'));
            var dayOfWeek = (date.getDay() + 1) % 7;
        }
    }
});
