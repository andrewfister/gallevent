var Event = Backbone.Model.extend({
    defaults: {
        'address1': '1234 Elm St',
        'address2': '',
        'city': 'San Francisco',
        'zipcode': '94109',
        'name': 'My Event',
        'description': 'A description of my event.',
        'start_date': '01/01/1970',
        'end_date': '01/01/1970',
        'ticket_price': 10.00,
    }
});

var EventCollection = Backbone.Collection.extend({
    model: Event,
    url: '/event',
});
