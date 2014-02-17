var Event = Backbone.Model.extend({
    defaults: {
        'address': '1234 Elm St, San Francisco, CA 94109',
        'street_number': '1234',
        'street': '1234 Elm St',
        'subpremise': '',
        'city': 'San Francisco',
        'zipcode': '94109',
        'name': 'My Event',
        'category': 'networking',
        'description': 'A description of my event.',
        'start_date': '01/01/1970',
        'start_time': '12:00pm',
        'end_date': '01/01/1970',
        'end_time': '12:00pm',
        'ticket_price': 10.00,
        'latitude': 0,
        'longitude': 0,
        'rsvp_limit': 0,
        'organizer_email': '',
        'organizer_phone': '555-555-5555',
        'organizer_url': 'http://www.gallevent.com'
    },
    
    initialize: function() {
        this.set({formatted_ticket_price: this.formattedTicketPrice()});
    },
    
    getAddress: function() {
        return this.get("address");
    },
    
    formattedTicketPrice: function() {
        var price = this.get("ticket_price");
        return price > 0 ? "$" + price : "FREE"; 
    },
    
    urlRoot: '/event/events'
});

var sortableDate = function(date, time){
   // var formatDate = date.split("/").reverse().join("");
   // var formatTime = parseInt(time.split(":").join("").slice(0,-2));
   // // Adjust for PM
   // formatTime += (time.indexOf("PM") === -1 ? 0 : 1200 - formatTime);
   // return formatDate + "" + formatTime;

   var formatDate = date.split("/");
   var formatTime = time.split(/[:AP]/);
   formatTime[0] = parseInt(formatTime[0], 10) + (parseInt(time.indexOf("AM") === -1, 10) && (formatTime[0] < 12) ? 0 : 12);
   date = new Date(formatDate[2], formatDate[0], formatDate[1], formatTime[0], formatTime[1]);
   return date.getTime();
};

var EventCollection = Backbone.Collection.extend({
    model: Event,
    url: '/event/events',

    categories: ['networking', 'education', 'fairs', 'athletic', 'art', 
                    'dancing', 'dining', 'nightlife'],

    initialize: function() {
        this.categoryCounts = {'networking': 0, 'education': 0, 'fairs': 0, 
                                'athletic': 0, 'art': 0, 'dancing': 0, 
                                'dining': 0, 'nightlife': 0};
        
        this._orderDateAscend = this.comparator;
        
        this.on("add", function(events) {
            _.each(events, function(event, index, items) {
                this.categoryCounts[event.attributes.category] += 1;
            }, this);
        }, this);
        
        this.on("reset", function(events) {
            _.each(this.categories, function(category, index, categories) {
                this.categoryCounts[category] = 0;
            }, this);
            
            _.each(events.models, function(event, index, items) {
                this.categoryCounts[event.attributes.category] += 1;
            }, this);
        }, this);
        
        this.on("remove", function(events) {
            _.each(events, function(event, index, items) {
                this.categoryCounts[event.attributes.category] -= 1;
            }, this);
        }, this);
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

var EventSearchCollection = EventCollection.extend({
    url: '/event/search/',
    
    storeLocally: function(searchParams, searchData, timestamp) {
        var galleventSearchCacheString = localStorage.getItem('gallevent_search_cache');
        
        if (galleventSearchCacheString === null)
        {
            
        }
        
        var galleventSearchCache = $.parseJSON(galleventSearchCacheString);
        galleventSearchCache.push({
        });
    }
});


