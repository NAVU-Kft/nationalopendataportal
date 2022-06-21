from ckan.common import _

def blog_t():
    return [
        {u'key': u'NEWS', u'label': _('Hírek')},
        {u'key': u'LEGAL_FRAMEWORK', u'label': _('Jogszabályi keretek')},
        {u'key': u'KNOWLEDGEBASE_MATERIALS', u'label': _('Vonatkozó joganyag')},
        {u'key': u'KNOWLEDGEBASE_METHODOLOGICAL', u'label': _('Módszertani segédanyagok')},
        {u'key': u'ANALYZES_NAVU', u'label': _('NAVÜ-ben készült elemzések')},
        {u'key': u'ANALYZES_ECON', u'label': _('Gazdasági és társadalmi hatások elemzése')},
        {u'key': u'ANALYZES_STAT', u'label': _('Statisztikák')},
        {u'key': u'CONFERENCES', u'label': _('Konferenciák')},
        {u'key': u'APPLICATIONS', u'label': _('Pályázatok')},
        {u'key': u'NEW_DATA_AND_FEATURES', u'label': _('Új adatok és funkciók')}
    ]

def get_blog_type_record(category_name_or_id):
    filtered = list(filter(lambda b: b['key'] == category_name_or_id or b['label'] == category_name_or_id , blog_t()))
    if len(filtered) > 0:
        return filtered[0]
    return None