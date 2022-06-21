ckan.module("cookie_consent", function ($) {
  return {
    initialize: function () {
      var cookieconsent = initCookieConsent();

      cookieconsent.run({
        current_lang: "en",
        force_consent: true,
        use_rfc_cookie: true,

        gui_options: {
          consent_modal: {
            layout: "bar", // box/cloud/bar
            position: "bottom center", // bottom/middle/top + left/right/center
            transition: "slide", // zoom/slide
          },
          settings_modal: {
            layout: "box", // box/bar
            // position: 'left',           // left/right
            transition: "slide", // zoom/slide
          },
        },

        languages: {
          en: {
            consent_modal: {
              title: this._('We use cookies'),
              description: this._('We use cookies and other tracking technologies to improve your browsing experience on our website, to show you personalized content and targeted ads, to analyze our website traffic, and to understand where our visitors are coming from.'),
              primary_btn: {
                text: this._("Accept all"),
                role: "accept_all", //'accept_selected' or 'accept_all'
              },
              secondary_btn: {
                text: this._("Change my preferences"),
                role: "settings", //'settings' or 'accept_necessary'
              },
            },
            settings_modal: {
              title: this._("Cookie preferences"),
              save_settings_btn: this._("Save preferences"),
              accept_all_btn: this._("Accept all"),
              reject_all_btn: this._("Reject all"), // optional, [v.2.5.0 +]
              close_btn_label: this._("Close"),
              blocks: [
                {
                  title: this._("We use cookies"),
                  description: this._("We use cookies and other tracking technologies to improve your browsing experience on our website, to show you personalized content and targeted ads, to analyze our website traffic, and to understand where our visitors are coming from."),
                },
                {
                  title: this._("Strictly necessary cookies"),
                  description: this._("Strictly necessary cookie description ... "),
                  toggle: {
                    value: "necessary",
                    enabled: true,
                    readonly: true,
                  },
                },
                {
                  title: this._("Analytics cookies"),
                  description: this._("Analytics cookie description ..."),
                  toggle: {
                    value: "analytics",
                    enabled: true,
                    readonly: false,
                  },
                },
              ],
            },
          },
        },
      });
    },
  };
});
