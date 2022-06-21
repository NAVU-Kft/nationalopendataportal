"use strict";

ckan.module("hutemplate_faq_search", function ($) {
  return {
    initialize: function () {
      //this.el -> div
      var $input = this.el.find(".search-input-group input");
      var $gyik = this.el.find(".info-list .panel");

      var filterElements = function () {
        var val = $input.val();
        if (val) {
          $gyik.each(function (index, panel) {
            var $panel = $(panel);
            var $collapse = $panel.find(".panel-collapse");
            var text = $panel.text();
            if (
              text.toLocaleLowerCase().indexOf(val.toLocaleLowerCase()) >= 0
            ) {
              $collapse.collapse("show");
            } else {
              $collapse.collapse("hide");
            }
          });
        } else {
          $gyik.each(function (index, panel) {
            var $panel = $(panel);
            var $collapse = $panel.find(".panel-collapse");
            $collapse.collapse("hide");
          });
        }
      };

      if ($input && $input[0]) {
        $input.on("keypress keydown blur", debounce(filterElements, 100));
      }
    },
  };
});

function debounce(callback, interval) {
  var debounceTimeoutId;
  return function (...args) {
    clearTimeout(debounceTimeoutId);
    debounceTimeoutId = setTimeout(() => callback.apply(this, args), interval);
  };
}
