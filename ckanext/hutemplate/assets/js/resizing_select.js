"use strict";

ckan.module("hutemplate_resizing_select", function ($) {
  return {
    /* options object can be extended using data-module-* attributes */
    options : {
			'arrowWidth': 0,
		},
    initialize: function () {
      //this.el -> select
      //create an empty clone of the original select
      var $clone = this.el.clone();
      $clone.children('option').remove();
      //create a new empty option
      var $opt = $('<option></option>');
      $opt.appendTo($clone);
      //insert clone to dom
      $clone.css('display', 'none');
      $clone.insertAfter(this.el);
      //set clone option to selected of the original select (this resizes the clone to the one option width)
      $opt.html(this.el.find('option:selected').text()); 
      
      $(this.el).width($clone.width()+this.options['arrowWidth']);
      $clone.remove();
    }
  };
});
