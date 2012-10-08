var Event = Backbone.Model.extend({
    defaults: {
        'address1': '1234 Elm St',
        'address2': '',
        'city': 'San Francisco',
        'zipcode': '94109',
        'name': 'My Event',
        'category': 'networking',
        'description': 'A description of my event.',
        'start_date': '01/01/1970',
        'start_time': '12:00',
        'end_date': '01/01/1970',
        'end_time': '12:00',
        'ticket_price': 10.00,
        'latitude': 0,
        'longitude': 0,
        'rsvp_limit': 0,
    },
    
    getAddress: function() {
        var address = this.get("address1") + ", ";
        var address2 = this.get("address2");
        
        if (address2.length > 0)
        {
            address += address2 + ", ";
        }
        
        address += this.get("city") + " " + this.get("zipcode");
        
        return address;
    },
    
    urlRoot: '/event/events',
});

var EventCollection = Backbone.Collection.extend({
    model: Event,
    url: '/event/events',

    initialize: function() {
        this._orderDateAscend = this.comparator;
    },

    comparator: function(e) {
        return sortableDate(e.get("start_date"), e.get("start_time"));
    },

    orderDateAscend: function() {
        console.log("Date Ascend");
        this.comparator = this._orderDateAscend;
        this.sort();
    },

    orderDateDescend: function() {
        console.log("Date Descend");
        this.comparator = this._orderDateDescend;
        this.sort();
    },

    orderCategory: function() {
        console.log("Order Category");
        this.comparator = this._orderCategory;
        this.sort();
    },

    _orderDateDescend: function(e) {
        return -sortableDate(e.get("start_date"), e.get("start_time"));
    },

    _orderCategory: function(e) {
        return e.get("category");
    }

});

var sortableDate = function(date, time){
   // var formatDate = date.split("/").reverse().join("");
   // var formatTime = parseInt(time.split(":").join("").slice(0,-2));
   // // Adjust for PM
   // formatTime += (time.indexOf("PM") === -1 ? 0 : 1200 - formatTime);
   // return formatDate + "" + formatTime;

   var formatDate = date.split("/");
   var formatTime = time.split(/[:AP]/);
   formatTime[0] = parseInt(formatTime[0]) + (parseInt(time.indexOf("AM") == -1) && (formatTime[0] < 12) ? 0 : 12);
   var date = new Date(formatDate[2], formatDate[0], formatDate[1], formatTime[0], formatTime[1]);
   return date.getTime();
};


