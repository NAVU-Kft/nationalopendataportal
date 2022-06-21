this.ckan = this.ckan || {};
this.ckan.pages = this.ckan.pages || {};

window.ckan.pages.override_config = {
  toolbarGroups: [
    { name: "clipboard", groups: ["clipboard", "undo"] },
    {
      name: "editing",
      groups: ["find", "selection", "spellchecker", "editing"],
    },
    { name: "basicstyles", groups: ["basicstyles", "cleanup"] },
    { name: "paragraph", groups: ["list", "indent", "blocks", "align"] },
    { name: "links", groups: ["links"] },
    { name: "insert", groups: ["insert"] },
    { name: "forms", groups: ["forms"] },
    { name: "styles", groups: ["styles"] },
    { name: "tools", groups: ["tools"] },
    { name: "document", groups: ["mode", "document", "doctools"] },
    "/",
    "/",
    { name: "colors", groups: ["colors"] },
    { name: "others", groups: ["others"] },
    { name: "about", groups: ["about"] },
  ],
  removeButtons:
    "Source,Save,NewPage,ExportPdf,Preview,Print,Templates,Font,FontSize,Format,BGColor,TextColor,Scayt,Subscript,Superscript,CreateDiv,BidiLtr,BidiRtl,Language,Flash,Smiley,SpecialChar,PageBreak,Iframe,Form,Checkbox,Radio,TextField,Textarea,Select,Button,ImageButton,HiddenField,About,ShowBlocks",
  extraPlugins: "justify", // Add extra plugins here (make sure to also load their js/css assets from your plugin)
  format_tags: "p;h1;h2;h3;h4",
  stylesSet: 'my_styles:/js/ckedit_styles.js',
  contentsCss: "/css/ckeditor-content.css",
  pasteFromWordRemoveFontStyles: true,
  allowedContent: {
    p:{
      styles: 'text-align',
      attributes: ['align']
    },
    div:{
      classes: 'page-split-title'
    },
    $1: {
      // Use the ability to specify elements as an object.
      elements: CKEDITOR.dtd,
      attributes: true,
      styles: false,
      classes: false,
    },
  },
  disallowedContent: "script; *[on*];",
  on: {
    afterPasteFromWord: function (params) {},
  },
};
