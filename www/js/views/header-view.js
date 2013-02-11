var HeaderView = Backbone.View.extend({
    id: "front-page",
    render: function() {
        $( "#date1" ).datepicker({ dateFormat: "mm/dd/yy", onSelect: this.changeDate, firstDay: 1, beforeShowDay: this.styleDateRange, minDate: new Date() });
        $("#time-span").change(this.changeDate);
		$("#header").slideToggle(600);
		
		if ($("#date1").attr('value').length == 0)
		{
		    var today = new Date();
		    /*var dd = ('0'+(today.getDate())).slice(-2);
		    var mm = ('0'+(today.getMonth()+1)).slice(-2);
		    var yyyy = today.getFullYear();
		    var formatToday = mm + '/' + dd + '/' + yyyy;*/
		    $("#date1").attr('value', $.datepicker.formatDate("mm/dd/yy", today));
		}
		
		if ($("#date2").attr('value').length == 0)
		{
		    $("#date2").attr('value', $( "#date1" ).attr('value'));
		}
    },
    
    changeDate: function() {
        if ($("#time-span").attr('value') == "day_of")
        {
            $("#date2").attr('value', $( "#date1" ).attr('value'));
        }
        else if ($("#time-span").attr('value') == "week_of")
        {
            var date = $.datepicker.parseDate('mm/dd/yy', $( "#date1" ).attr('value'));
            var dayOfWeek = (date.getDay() - 1) % 7;
            date.setDate(date.getDate() - dayOfWeek);
            var date2 = new Date();
            date2.setDate(date.getDate() + 6);
            
            $("#date1").attr('value', $.datepicker.formatDate('mm/dd/yy', date));
            $("#date2").attr('value', $.datepicker.formatDate('mm/dd/yy', date2));
        }
        else if ($("#time-span").attr('value') == "weekend_of")
        {
            var date = $.datepicker.parseDate('mm/dd/yy', $( "#date1" ).attr('value'));
            var dayOfWeek = (date.getDay() - 1) % 7;
            date.setDate(date.getDate() - dayOfWeek + 4);
            var date2 = new Date();
            date2.setDate(date.getDate() + 2);
            
            $("#date1").attr('value', $.datepicker.formatDate('mm/dd/yy', date));
            $("#date2").attr('value', $.datepicker.formatDate('mm/dd/yy', date2));
        }
    },
    
    styleDateRange: function(date) {
        var now = new Date();
        var today = new Date(now.getFullYear(), now.getMonth(), now.getDay());
        var selectable = date.valueOf() >= today.valueOf();
        var style = "";
        var date1 = $.datepicker.parseDate('mm/dd/yy', $( "#date1" ).attr('value'));
        var date2 = $.datepicker.parseDate('mm/dd/yy', $( "#date2" ).attr('value'));
        
        if (date.valueOf() >= date1.valueOf() && date.valueOf() <= date2.valueOf())
        {
            style = "ui-datepicker-today";
        }
        else if (date.valueOf() == today.valueOf())
        {
            style = "";
        }
        
        return [selectable, style];
    }
});
