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
    }
});

var EventCollection = Backbone.Collection.extend({
    model: Event,
    url: '/event/events'
});
