"use strict";

ckan.module("hutemplate_facet_search_button", function ($) {
  return {
    initialize: function () {
        // this.el -> button
        this.el.on('click tap', function(){
            var $filtersRoot = $(this).parents('.filters');
            var queryStr = $filtersRoot.find('input, select').serialize();
            window.location.search = '?' + queryStr;
        })
    }
  }
});

ckan.module("hutemplate_facet_clear_button", function ($) {
    return {
      initialize: function () {
          // this.el -> button
          this.el.on('click tap', function(){
            window.location.search = '';
        })
      }
    }
  });