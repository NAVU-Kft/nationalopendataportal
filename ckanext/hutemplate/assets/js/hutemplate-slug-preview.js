this.ckan.module('hutemplate-slug-preview-created', {
  initialize: function () {
    var sandbox = this.sandbox;
    var options = this.options;
    var el = this.el;

    sandbox.subscribe('slug-preview-created', function (preview) {
      // Append the preview string after the target input.
      var infoBlock = el.parent().find('.info-block');
      if(infoBlock && infoBlock.length > 0){
        infoBlock.after(preview);
      }else{
        el.after(preview);
      }
    });

    // Make sure there isn't a value in the field already...
    if (el.val() == '') {
      // Once the preview box is modified stop watching it.
      sandbox.subscribe('slug-preview-modified', function () {
        el.off('.slug-preview');
      });

      // Watch for updates to the target field and update the hidden slug field
      // triggering the "change" event manually.
      el.on('keyup.slug-preview input.slug-preview', function (event) {
        sandbox.publish('slug-target-changed', this.value);
        //slug.val(this.value).trigger('change');
      });
    }
  }
});