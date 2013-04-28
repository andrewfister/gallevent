var SearchView = Backbone.View.extend({
    id: "top-search",
    
    render: function() {
        $("#date").datepicker({ dateFormat: "mm/dd/yy", onSelect: this.changeDate, firstDay: 1, beforeShowDay: this.styleDates, minDate: new Date(), constrainInput: true });
        $("#time-span").change(this.changeTimeSpan.bind(this));
        
		if ($("#date").attr('value').length === 0)
		{
		    var today = new Date();
		    var todayText = $.datepicker.formatDate("mm/dd/yy", today);
		    $("#date").attr('value', todayText);
		    $("#date1").attr('value', todayText);
		    $("#date2").attr('value', todayText);
		}
		
		if ($("#date1").attr('value').length === 0)
		{
		    $("#date1").attr('value', $( "#date" ).attr('value'));
		}
		
		if ($("#date2").attr('value').length === 0)
		{
		    $("#date2").attr('value', $( "#date1" ).attr('value'));
		}
		
		this.changeDate();
		
		$('.btn-search').click(this.submitSearch.bind(this));
		$('#map-latitude').change(this.submitSearch.bind(this));
		$('#map-longitude').change(this.submitSearch.bind(this));
    },
    
    changeTimeSpan: function() {
        this.changeDate();
        $('#date').datepicker('show');
    },
    
    changeDate: function() {
        var date;
        var dayOfWeek;
        var date2;
    
        if ($("#time-span").attr('value') === "day_of")
        {
            $("#date1").attr('value', $( "#date" ).attr('value'));
            $("#date2").attr('value', $( "#date" ).attr('value'));
        }
        else if ($("#time-span").attr('value') === "week_of")
        {
            date = $.datepicker.parseDate('mm/dd/yy', $( "#date" ).attr('value'));
            dayOfWeek = (date.getDay() + 6) % 7;
            date.setDate(date.getDate() - dayOfWeek);
            date2 = new Date(date);
            date2.setDate(date.getDate() + 6);
            
            $("#date1").attr('value', $.datepicker.formatDate('mm/dd/yy', date));
            $("#date2").attr('value', $.datepicker.formatDate('mm/dd/yy', date2));
        }
        else if ($("#time-span").attr('value') === "weekend_of")
        {
            date = $.datepicker.parseDate('mm/dd/yy', $( "#date" ).attr('value'));
            dayOfWeek = (date.getDay() + 6) % 7;
            date.setDate(date.getDate() - dayOfWeek + 4);
            date2 = new Date(date);
            date2.setDate(date.getDate() + 2);
            
            $("#date1").attr('value', $.datepicker.formatDate('mm/dd/yy', date));
            $("#date2").attr('value', $.datepicker.formatDate('mm/dd/yy', date2));
        }
    },
    
    styleDates: function(date) {
        var now = new Date();
        var today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        var selectable = date.valueOf() >= today.valueOf();
        var style = "";
        var date1 = $.datepicker.parseDate('mm/dd/yy', $( "#date1" ).attr('value'));
        var date2 = $.datepicker.parseDate('mm/dd/yy', $( "#date2" ).attr('value'));
        
        if (date.valueOf() >= date1.valueOf() && date.valueOf() <= date2.valueOf())
        {
            style = "ui-datepicker-today";
        }
        
        return [selectable, style];
    },
    
    submitSearch: function() {
        var searchCollection = new EventSearchCollection();
        var serializedSearch = $('#top-search').serializeArray();
        var searchData = {};
        var i;
        for (i = 0; i < serializedSearch.length; i++)
        {
            searchData[serializedSearch[i].name] = serializedSearch[i].value;
        }
        
        if (searchData.q.length === 0)
        {
            searchData.q = "default";
        }
        
        searchCollection.fetch({
            data: searchData, 
            success: function(collection, response, options) {
                this.collection.reset(response);
            }.bind(this)
        });
    }
});