"use strict";

ckan.module("hutemplate_facet_list", function ($) {
  return {
    initialize: function () {
      //this.el -> section
      var $input = this.el.find(".facet-search");
      var $liArr = this.el.find("ul li");

      var $readMore = this.el.find("a.read-more");
      var $nav = this.el.find("nav");

      var filterElements = function () {
        var val = $input.val();
        if (val) {
          var foundCount = 0;
          $liArr.each(function (index, li) {
            var $li = $(li);
            var text = $li.find(".item-label").text();
            if (
              text.toLocaleLowerCase().indexOf(val.toLocaleLowerCase()) >= 0
            ) {
              $li.removeClass("hidden");
              foundCount++;
            } else {
              $li.addClass("hidden");
            }
          });
          if (foundCount > 4) {
            $readMore.removeClass("hidden");
          } else {
            $readMore.addClass("hidden");
          }
        } else {
          $readMore.removeClass("hidden");
          $liArr.removeClass("hidden");
        }
      };

      var toggleMore = function () {
        $nav.toggleClass("opened");
        if ($nav.hasClass("opened")) {
          $readMore.text($readMore.data("opened-text"));
        } else {
          $readMore.text($readMore.data("closed-text"));
        }
      };

      if ($readMore && $readMore[0]) {
        $readMore.on("click", debounce(toggleMore, 100));
      }

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
