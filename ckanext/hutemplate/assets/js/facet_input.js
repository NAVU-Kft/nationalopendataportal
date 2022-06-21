"use strict";

ckan.module("hutemplate_facet_input", function ($) {
    return {
      initialize: function () {
          var $input = $(this.el);
          $input.blur(function(){
            var name = $(this).attr('name');
            var val = $(this).val();
            window.location.href = updateURLParameter(window.location.href, name, val)
          });
      }
    };
});

function updateURLParameter(url, param, paramVal)
{
    var TheAnchor = null;
    var newAdditionalURL = "";
    var tempArray = url.split("?");
    var baseURL = tempArray[0];
    var additionalURL = tempArray[1];
    var temp = "";

    if (additionalURL) 
    {
        let tmpAnchor = additionalURL.split("#");
        let TheParams = tmpAnchor[0];
            TheAnchor = tmpAnchor[1];
        if(TheAnchor)
            additionalURL = TheParams;

        tempArray = additionalURL.split("&");
        for (let el of tempArray)
        {
            let key = el.split('=')[0]
            if(key != param)
            {
                newAdditionalURL += temp + el;
                temp = "&";
            }
        }        
    }
    else
    {
        let tmpAnchor = baseURL.split("#");
        let TheParams = tmpAnchor[0];
            TheAnchor  = tmpAnchor[1];

        if(TheParams)
            baseURL = TheParams;
    }

    if(TheAnchor)
        paramVal += "#" + TheAnchor;
    var rows_txt = "";
    if(paramVal){
        rows_txt += temp + "" + param + "=" + paramVal;
    }
    return baseURL + "?" + newAdditionalURL + rows_txt;
}