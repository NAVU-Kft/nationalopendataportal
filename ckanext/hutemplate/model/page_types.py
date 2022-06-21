from ckan.common import _

def page_t():
    return [
        {u'key': u'DATA_REQUEST', u'label': _('Data Request')},
        {u'key': u'ABOUT', u'label': _('About Open Data Portal')},
        {u'key': u'STANDARDS_VOCABULARIES', u'label': _('International standards')},
        {u'key': u'PRIVACY_POLICY', u'label': _('Privacy policy')},
        {u'key': u'DISCLAIMERS', u'label': _('Disclaimers')},
        {u'key': u'CONTACT', u'label': _('Contact')},
        {u'key': u'IMPRINT', u'label': _('Imprint')},
        {u'key': u'PURPOSE', u'label': _('Purpose of the portal')},
        {u'key': u'NEWS', u'label': _('News')}
    ]

def get_page_type_record(category_name_or_id):
    filtered = list(filter(lambda b: b['key'] == category_name_or_id or b['label'] == category_name_or_id , page_t()))
    if len(filtered) > 0:
        return filtered[0]
    return None
