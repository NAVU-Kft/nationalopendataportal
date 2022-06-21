import logging
from types import DynamicClassAttribute
import click
import re
import traceback

from rdflib import Graph, URIRef, Literal
from rdflib.resource import Resource
from rdflib.namespace import Namespace, SKOS, DC, RDF
from ckanext.dcat.profiles import namespaces, DCT
from ckan.lib.base import config
import ckan.plugins.toolkit as toolkit
from ckan.model import Session
from ckanext.hutemplate.model import HutemplateTagVocabulary 

log = logging.getLogger(__name__)
EUVOC = Namespace('http://publications.europa.eu/ontology/euvoc#')

@click.group()
def hutemplate():
    pass

@hutemplate.command()
def initdb():
    click.echo('Running command initdb')
    from ckanext.hutemplate.model import setup as db_setup
    db_setup()



    Session.execute('update ckanext_pages set extras = replace(extras, \'\\u00e1\', \'á\')')
    Session.execute('update ckanext_pages set extras = replace(extras, \'\\u00ed\', \'í\')')
    Session.execute('update ckanext_pages set extras = replace(extras, \'\\u0171\', \'ű\')')
    Session.execute('update ckanext_pages set extras = replace(extras, \'\\u0151\', \'ő\')')
    Session.execute('update ckanext_pages set extras = replace(extras, \'\\u00fc\', \'ü\')')
    Session.execute('update ckanext_pages set extras = replace(extras, \'\\u00f6\', \'ö\')')
    Session.execute('update ckanext_pages set extras = replace(extras, \'\\u00fa\', \'ú\')')
    Session.execute('update ckanext_pages set extras = replace(extras, \'\\u00f3\', \'ó\')')
    Session.execute('update ckanext_pages set extras = replace(extras, \'\\u00e9\', \'é\')')

    Session.execute('update ckanext_pages set extras = replace(extras, \'\\u00c1\', \'Á\')')
    Session.execute('update ckanext_pages set extras = replace(extras, \'\\u00cd\', \'Í\')')
    Session.execute('update ckanext_pages set extras = replace(extras, \'\\u0170\', \'Ű\')')
    Session.execute('update ckanext_pages set extras = replace(extras, \'\\u0150\', \'Ő\')')
    Session.execute('update ckanext_pages set extras = replace(extras, \'\\u00dc\', \'Ü\')')
    Session.execute('update ckanext_pages set extras = replace(extras, \'\\u00d6\', \'Ö\')')
    Session.execute('update ckanext_pages set extras = replace(extras, \'\\u00da\', \'Ú\')')
    Session.execute('update ckanext_pages set extras = replace(extras, \'\\u00d3\', \'Ó\')')
    Session.execute('update ckanext_pages set extras = replace(extras, \'\\u00c9\', \'É\')')
    
    
    #page type update
    # we duplicate the page_t array from page_types model, because the array in the model contains translated labels, not the strings from the original array
    page_t = [
        {u'key': u'DATA_REQUEST', u'label': u'Adatigénylés'},
        {u'key': u'ABOUT', u'label': u'Közadatportálról'},
        {u'key': u'STANDARDS_VOCABULARIES', u'label': u'Szabványok, szókészletek'},
        {u'key': u'PRIVACY_POLICY', u'label': u'Adatvédelmi szabályzat'},
        {u'key': u'DISCLAIMERS', u'label': u'Jogi felelősség nyilatkozatok'},
        {u'key': u'CONTACT', u'label': u'Kapcsolat'},
        {u'key': u'IMPRINT', u'label': u'Impresszum'},
        {u'key': u'PURPOSE', u'label': u'Portál célja'}
    ]
    for page_row in page_t:
        s = 'UPDATE ckanext_pages SET extras = REPLACE(extras,  \'"page_subtype": "'+page_row['label']+'"\', \'"page_subtype": "'+page_row['key']+'"\')'
        Session.execute(s)

    #blog type update
    blog_t = [
        {u'key': u'NEWS', u'label': u'Hírek'},
        {u'key': u'LEGAL_FRAMEWORK', u'label': u'Jogszabályi keretek'},
        {u'key': u'KNOWLEDGEBASE_MATERIALS', u'label': u'Vonatkozó joganyag'},
        {u'key': u'KNOWLEDGEBASE_METHODOLOGICAL', u'label': u'Módszertani segédanyagok'},
        {u'key': u'ANALYZES_NAVU', u'label': u'NAVÜ-ben készült elemzések'},
        {u'key': u'ANALYZES_ECON', u'label': u'Gazdasági és társadalmi hatások elemzése'},
        {u'key': u'ANALYZES_STAT', u'label': u'Statisztikák'},
        {u'key': u'CONFERENCES', u'label': u'Konferenciák'},
        {u'key': u'APPLICATIONS', u'label': u'Pályázatok'},
        {u'key': u'NEW_DATA_AND_FEATURES', u'label': u'Új adatok és funkciók'}
    ]
    for blog_row in blog_t:
        s = 'UPDATE ckanext_pages SET extras = REPLACE(extras,  \'"blog_type": "'+blog_row['label']+'"\', \'"blog_type": "'+blog_row['key']+'"\')'
        Session.execute(s)

    Session.commit()

    return

# http://publications.europa.eu/resource/authority/data-theme -> group
# http://publications.europa.eu/resource/authority/dataset-type -> dataset-types
# http://publications.europa.eu/resource/authority/place -> spatials (HUN_ előszűrés)
# http://publications.europa.eu/resource/authority/atu/HUN -> spatials (2 szint?)
# http://publications.europa.eu/resource/authority/access-right -> access-rights
# http://publications.europa.eu/resource/authority/frequency -> frequencies
# http://publications.europa.eu/resource/authority/language -> languages (ISO_639_1 nyelvek)
# http://publications.europa.eu/resource/authority/file-type -> file-types
# https://www.iana.org/assignments/media-types/media-types.xml -> media-types

@hutemplate.command()
@click.option('--force', help='Force load', default=False)
def load_all(force):
    load_vocabulary_inner('http://publications.europa.eu/resource/authority/data-theme', 'group', force=force)
    load_vocabulary_inner('http://publications.europa.eu/resource/authority/dataset-type', 'dataset-types', force=force)
    load_access_rights_inner(force=force)
    load_vocabulary_inner('http://publications.europa.eu/resource/authority/frequency', 'frequencies', force=force)
    load_availability_inner(force=force)
    load_vocabulary_inner('http://publications.europa.eu/resource/authority/place', 'spatials', filter='HUN_', tag_lang='hu', force=force)
    load_vocabulary_inner('http://publications.europa.eu/resource/authority/atu/HUN', 'spatials', depth = 2, tag_lang='hu', add_self=[True, True], force=force) # depth=3 esetén a megyei jogú városokat is felveszi mégegyszer
    load_vocabulary_inner('http://publications.europa.eu/resource/authority/file-type', 'file-types', force=force)
    load_adms_statuses_inner(force=force)
    load_temporal_inner(force=force)

    load_languages_inner('languages', force=force)

@hutemplate.command()
@click.option('--url', help='URL to a resource', required=True)
@click.option('--name', help='Name of vocabulary', required=True)
@click.option('--force', help='Force load', default=False)
def load_vocabulary(url, name, force):
    load_vocabulary_inner(url, name, force=force)

@hutemplate.command()
@click.option('--url', help='URL to a resource', required=True)
@click.option('--force', help='Force load', default=False)
def load_languages(url, force):
    load_languages_inner('languages', url, force=force)

@hutemplate.command()
@click.option('--force', help='Force load', default=False)
def load_availability(force):
    load_availability_inner(force=force)

@hutemplate.command()
@click.option('--force', help='Force load', default=False)
def load_adms_statuses(force):
    load_adms_statuses_inner(force=force)

@hutemplate.command()
@click.option('--force', help='Force load', default=False)
def load_temporal(force):
    load_temporal_inner(force=force)

@hutemplate.command()
@click.option('--force', help='Force load', default=False)
def load_access_rights(force):
    load_access_rights_inner(force=force)

@hutemplate.command()
@click.option('--url', help='URL to a resource', required=True)
@click.option('--force', help='Force load', default=False)
def load_eurovoc(url, force):
    load_eurovoc_inner(url, force=force)
    #load_eurovoc_inner('http://eurovoc.europa.eu/100142', force=force)
    #load_eurovoc_inner('http://eurovoc.europa.eu/100143', force=force)
    #load_eurovoc_inner('http://eurovoc.europa.eu/100144', force=force)
    #load_eurovoc_inner('http://eurovoc.europa.eu/100145', force=force)
    #load_eurovoc_inner('http://eurovoc.europa.eu/100146', force=force)
    #load_eurovoc_inner('http://eurovoc.europa.eu/100147', force=force)
    #load_eurovoc_inner('http://eurovoc.europa.eu/100148', force=force)
    #load_eurovoc_inner('http://eurovoc.europa.eu/100149', force=force)
    #load_eurovoc_inner('http://eurovoc.europa.eu/100150', force=force)
    #load_eurovoc_inner('http://eurovoc.europa.eu/100151', force=force)
    #load_eurovoc_inner('http://eurovoc.europa.eu/100152', force=force)
    #load_eurovoc_inner('http://eurovoc.europa.eu/100153', force=force)
    #load_eurovoc_inner('http://eurovoc.europa.eu/100154', force=force)
    #load_eurovoc_inner('http://eurovoc.europa.eu/100155', force=force)
    #load_eurovoc_inner('http://eurovoc.europa.eu/100156', force=force)
    #load_eurovoc_inner('http://eurovoc.europa.eu/100157', force=force)
    #load_eurovoc_inner('http://eurovoc.europa.eu/100158', force=force)
    #load_eurovoc_inner('http://eurovoc.europa.eu/100159', force=force)
    #load_eurovoc_inner('http://eurovoc.europa.eu/100160', force=force)
    #load_eurovoc_inner('http://eurovoc.europa.eu/100161', force=force, depth=2, add_self=[False, True])
    #load_eurovoc_inner('http://eurovoc.europa.eu/100162', force=force)

def load_eurovoc_inner(url=None, force=False):
    g = _try_parse_graph_urls([url, 'src/ckanext-hutemplate/ckanext/hutemplate/vocabularies/eurovoc-skos-ap-eu.rdf', 'src_extensions/ckanext-hutemplate/ckanext/hutemplate/vocabularies/eurovoc-skos-ap-eu.rdf'])
    if g == None:
        return
    
    dict = {}
    ckan_offered_languages = config.get('ckan.locales_offered', 'hu').split(' ')

    # http://eurovoc.europa.eu/domains
    for node,_pred,_conc in g.triples( (URIRef("http://eurovoc.europa.eu/domains"), SKOS.hasTopConcept, None ) ):
        #Domains (pl 52 KÖRNYEZET)
        for node2,_pred2,_conc2 in g.triples( (None, EUVOC.domain, _conc ) ):
            # 5211 természetes környezet
            for node3,_pred3,_conc3 in g.triples( (node2, SKOS.hasTopConcept, None ) ):
                # geofizikai környezet
                identifier = str(_conc3)
                if identifier not in dict:
                    dict[identifier] = {}
                for pref_label in g.objects(_conc3, SKOS.prefLabel):
                    lang = pref_label.language
                    label = pref_label.value
                    if lang in ckan_offered_languages:
                        dict[identifier][lang] = label
                if len(dict[identifier]) != 2:
                    dict.pop(identifier, None)
                
    for key, value in dict.items():
        dict2 = {}
        dict2[key] = value
        do_load_vocabulary(key, dict2, 'eurovoc', 'hu')

def load_languages_inner(name, url=None, force=False):
    baseurl = 'http://publications.europa.eu/resource/authority/language'
    click.echo(f"Loading vocabulary {name}")
    click.echo(f"Loading vocabulary from file: {url}")

    dict = {}
    g = _try_parse_graph_urls([url, 'src/ckanext-hutemplate/ckanext/hutemplate/vocabularies/languages-skos.rdf', 'src_extensions/ckanext-hutemplate/ckanext/hutemplate/vocabularies/languages-skos.rdf'])
    
    if g == None:
        return

    ckan_offered_languages = config.get('ckan.locales_offered', 'hu').split(' ')
    predicate = SKOS.inScheme 
    if (None, SKOS.broader, URIRef(url)) in g:
        predicate = SKOS.broader

    for node,_pred,_conc in g.triples((None, predicate, URIRef(baseurl))):
        identifier = ''
        for id in g.objects(node, DC.identifier):
            identifier = id.value
            break

        if identifier not in dict:
            dict[identifier] = {}

        for pref_label in g.objects(node, SKOS.prefLabel):
            lang = pref_label.language
            label = pref_label.value
            if lang in ckan_offered_languages:
                dict[identifier][lang] = label
        if len(dict[identifier]) != 2:
            dict.pop(identifier, None)

    for key, value in dict.items():
        dict2 = {}
        dict2[key] = value
        do_load_vocabulary(baseurl+'/'+key, dict2, 'languages', 'hu')

def load_vocabulary_inner(url, name, filter=None, depth=2, tag_lang='key', add_self=[False, True], force=False, predicate=None):
    click.echo(f"{depth} Loading vocabulary {name}")
    click.echo(f"{depth} Loading vocabulary from url: {url}")
    
    dict = {}
    
    g = _parse_graph(url)
    if g == None:
        return

    ckan_offered_languages = config.get('ckan.locales_offered', 'hu').split(' ')
    
    actualPredicate = None
    if predicate:
        actualPredicate = predicate[len(predicate)-depth]
    
    if not actualPredicate:
        actualPredicate = SKOS.inScheme 
        if (None, SKOS.broader, URIRef(url)) in g:
            actualPredicate = SKOS.broader


    click.echo(f"{actualPredicate}")

    if add_self[len(add_self)-depth]:
        identifier = ''
        for id in g.objects(None, DC.identifier):
            identifier = id.value
            break

        if identifier not in dict:
            dict[identifier] = {}

        for pref_label in g.objects(None, SKOS.prefLabel):
            lang = pref_label.language
            label = pref_label.value
            if lang in ckan_offered_languages:
                dict[identifier][lang] = label

    for node,_pred,_conc in g.triples((None, actualPredicate, URIRef(url))):
        if filter != None and url+'/'+filter not in node:
            continue

        if not force and url_exists(node):
            click.echo(f"{depth} url exists, skipping {node}")
            continue

        if depth > 1:
            load_vocabulary_inner(node, name, depth=depth-1, tag_lang=tag_lang, add_self=add_self, force=force, predicate=predicate)

    if name == 'group':
        load_groups(dict, url)
    else:
        do_load_vocabulary(url, dict, name, tag_lang)

def do_load_vocabulary(url, dict, name, tag_lang):
    user = toolkit.get_action('get_site_user')({'ignore_auth': True}, {})
    vocab = None
    if name:
        vocab = create_vocabulary(name, user)
    
    for key, value in dict.items():
        if key == 'OP_DATPRO':
            continue

        huterm = get_hu_term(value)
        if tag_lang == 'key':
            display_name = key
        else:
            display_name = value[tag_lang] if tag_lang in list(value.keys()) else huterm
        create_tag(key, display_name, vocab, user, url)
        save_translations(display_name, value, user)

def load_temporal_inner(force=False):
    baseurl = 'http://publications.europa.eu/resource/authority/timeperiod'
    dict = {'SEC': {'hu': 'másodperc', 'en': 'Second'}, 'MIN': {'hu': 'perc', 'en': 'Minute'}, 'HOUR': {'hu': 'óra', 'en': 'Hour'}, 'DAY': {'hu': 'nap', 'en': 'Day'}, 'WEEK': {'hu': 'hét', 'en': 'Week'}, 'MONTH': {'hu': 'hónap', 'en': 'Month'}, 'QUARTER': {'hu': 'negyedév', 'en': 'Quarter year'}, 'YEAR_HALF': {'hu': 'félév', 'en': 'Half year'}, 'YEAR': {'hu': 'év', 'en': 'Year'}}
    for key, value in dict.items():
        dict2 = {}
        dict2[key] = value
        do_load_vocabulary(baseurl+'/'+key, dict2, 'temporal', 'key')

def load_access_rights_inner(force=False):
    baseurl = 'http://publications.europa.eu/resource/authority/access-right'
    dict = {'NON_PUBLIC': {'hu': 'Nem publikus', 'en': 'non-public'}, 
    'PUBLIC': {'hu': 'Publikus', 'en': 'public'}, 
    'RESTRICTED': {'hu': 'Korlátozott', 'en': 'restricted'}, 
    'SENSITIVE': {'hu': 'Érzékeny', 'en': 'sensitive'}, 
    'CONFIDENTIAL': {'hu': 'Bizalmas', 'en': 'confidential'}}
    for key, value in dict.items():
        dict2 = {}
        dict2[key] = value
        do_load_vocabulary(baseurl+'/'+key, dict2, 'access-rights', 'key')

def load_adms_statuses_inner(force=False):
    baseurl = 'http://purl.org/adms/status'
    dict = {'Completed': {'hu': 'befejezett', 'en': 'Completed'}, 'Deprecated': {'hu': 'elavult', 'en': 'Deprecated'}, 'UnderDevelopment': {'hu': 'fejlesztés alatt', 'en': 'Under development'}, 'Withdrawn': {'hu': 'visszavont', 'en': 'Withdrawn'}}
    for key, value in dict.items():
        dict2 = {}
        dict2[key] = value
        do_load_vocabulary(baseurl+'/'+key, dict2, 'adms_statuses', 'key')

def load_availability_inner(force=False):
    baseurl = 'http://data.europa.eu/r5r/availability'
    dict = {'temporary': {'hu': 'Ideiglenes', 'en': 'Temporary'}, 'experimental': {'hu': 'Kísérleti', 'en': 'Experimental'}, 'available': {'hu': 'Elérhető', 'en': 'Available'}, 'stable': {'hu': 'Állandó', 'en': 'Stable'}}
    for key, value in dict.items():
        dict2 = {}
        dict2[key] = value
        do_load_vocabulary(baseurl+'/'+key, dict2, 'availability', 'key')

def load_groups(dict, url, force=False):
    user = toolkit.get_action('get_site_user')({'ignore_auth': True}, {})
    group_create = toolkit.get_action('group_create')
    group_show = toolkit.get_action('group_show')
    group_update = toolkit.get_action('group_update')
    for key, value in dict.items():
        if key == 'OP_DATPRO':
            continue
        
        huterm = get_hu_term(value)
        try:
            g = group_show({'user': user['name']}, {'id': key.lower()})
            g['schema_url'] = url
            group_update({'user': user['name']}, g)
        except toolkit.ObjectNotFound:
            g = group_create({'user': user['name']}, {'name': key.lower(), 'title': huterm, 'schema_url': url })
        save_translations(huterm, value, user)
        

def create_tag(key, display_name, vocab, user, url):
    vocab_id = None
    if vocab:
        vocab_id = vocab['id']

    context = {'user': user['name']}
    if len(display_name) < 2:
        display_name = '_'+display_name+'_'
    display_name = re.sub(r'[^\w \-_\.áÁíÍűŰőŐüÜöÖúÚőÓéÉ]', '', display_name)        
    
    data = {'name': display_name, 'vocabulary_id': vocab_id}

    tag_create = toolkit.get_action('tag_create')
    tag_show = toolkit.get_action('tag_show')
    try:
        param = {'id': display_name, 'vocabulary_id': vocab_id}
        tag = tag_show(context, param)
    except toolkit.ObjectNotFound:
        tag = tag_create(context, data)
    
    existing = HutemplateTagVocabulary.by_tag_id(tag['id'])
    if existing is None:
        HutemplateTagVocabulary(tag['id'], vocab_id, display_name, url).persist()
    else:
        existing.url = url
        existing.vocabulary_id = vocab_id
        existing.persist()
    
def url_exists(url):
    existing = HutemplateTagVocabulary.by_url(url)
    return existing is not None

def get_hu_term(value):
    huterm = value['en']
    if 'hu' in value:
        huterm = value['hu']
    return huterm

def save_translations(huterm, value, user):
    term_translation_update = toolkit.get_action('term_translation_update')
    for lang, translation in value.items():
        term_translation_update({'user': user['name']}, {'term': huterm, 'term_translation': translation, 'lang_code': lang})

def create_vocabulary(vocabulary_id, user):
    context = {'user': user['name']}
    try:
        data = {'id': vocabulary_id}
        return toolkit.get_action('vocabulary_show')(context, data)
    except toolkit.ObjectNotFound:
        data = {'name': vocabulary_id}
        return toolkit.get_action('vocabulary_create')(context, data)

def _try_parse_graph_urls(filenames):
    for filename in filenames:
        try:
            g = _parse_graph(None, filename)
            return g
        except Exception as e:
            continue
    
    log.error("ERROR: Problem occurred while retrieving the document")
    click.echo("ERROR: Problem occurred while retrieving the document")
    return None

def _parse_graph(url, filename=None):
    g = Graph()
    for prefix, namespace in namespaces.items():
        g.bind(prefix, namespace)
    fargs = {}
    if url:
        fargs['location'] = url
    elif filename:
        fargs['source'] = filename

    fargs['format'] = 'xml'
    click.echo(f"loading with {fargs}")
    
    g.parse(**fargs)
    
    return g