$(function() {
  // for storing states
  var states = [];

  // cache some elems
  var $states = $('#state');
  var $stateList = $('#state-list');
  
  // hide the dropdown and pull values
  $states.hide().find('option').each(function() {
    var $this = $(this);
    var val = $this[0].value;
    if (val !== '') {
      states.push({ 
        value: val, 
        label: $this[0].text || $this.text() 
      });
    }
  });

  // force loading of value
  var curState = $states.val();
  if (curState.length) {
    var len = states.length;
    for (i = 0; i < len; i++) {
      if (states[i].value == curState) {
        $stateList.val(states[i].label);
      }
    }
  }
  
  // swap out the dropdown for a hidden elem
  $states.remove();
  $states = $('<input type="hidden" id="state" name="state" />').insertAfter($stateList);
  
  // show the input
  $stateList.show();
  
  // handle autocompletion
  $stateList.autocomplete({ 
    minLength: 0,
    source: function(request, response) {
      var matcher = new RegExp($.ui.autocomplete.escapeRegex(request.term), 'i');
      response(
        $.grep(states, function(value) {
          return matcher.test(value.value) || matcher.test(value.label);
        }
      ));
    },
    focus: function(event, ui) { 
      return false;
    },
    select: function(event, ui) {
      $stateList.val(ui.item.label);
      $states.val(ui.item.value);
      return false;
    }
  });
});