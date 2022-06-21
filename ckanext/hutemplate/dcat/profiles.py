import logging
import ckan.logic as logic
import ckan.model as model
from rdflib.namespace import Namespace, XSD, RDF, SKOS
from ckanext.dcat.profiles import RDFProfile, DCAT, LOCN, VCARD, DCT, FOAF, ADMS, OWL, SCHEMA, TIME
from ckanext.dcat.utils import catalog_uri, dataset_uri, resource_uri
from rdflib import URIRef, BNode, Literal
from ckanext.hutemplate.model import HutemplateTagVocabulary 
import ckan.plugins.toolkit as toolkit

log = logging.getLogger(__name__)

THEME_BASE_URI = 'http://publications.europa.eu/resource/authority/data-theme/'
FORMAT_BASE_URI = 'http://publications.europa.eu/resource/authority/file-type/'
MEDIA_TYPE_BASE_URI = 'https://www.iana.org/assignments/media-types/'

DEFAULT_VOCABULARY_KEY = 'OP_DATPRO'
DEFAULT_THEME_KEY = DEFAULT_VOCABULARY_KEY
DEFAULT_FORMAT_CODE = DEFAULT_VOCABULARY_KEY

hu_lang = 'hu'
DCATAP = Namespace('http://data.europa.eu/r5r/')
class HungarianDCATAPProfile(RDFProfile):
    def parse_dataset(self, dataset_dict, dataset_ref):
        return dataset_dict

    def graph_from_dataset(self, dataset_dict, dataset_ref):
        self.g.bind('dcatap', DCATAP)
        # dct:title from title (dcat plugin)
        # dct:description from description (dcat plugin)
        # dcat:contactPoint from maintainer and maintainer_email
        self.add_contact_point(dataset_dict, dataset_ref)
        # dcat:keywords from keywords (dcat plugin)
        #self.modify_keywords(dataset_dict, dataset_ref)
        # dct:publisher Extra fields (email and homepage) from organization
        self.add_publisher_extra(dataset_dict, dataset_ref)
        # dct:spatial
        self.modify_spatial(dataset_dict, dataset_ref)
        # dct:temporal from temporal_start and temporal_end (dcat plugin)
        # dact:theme from group
        self.add_themes_from_groups(dataset_dict, dataset_ref)
        # dct:accessRights
        self.modify_access_rights(dataset_dict, dataset_ref)
        # dct:creator from author and author_email
        self.add_creator(dataset_dict, dataset_ref)
        # dct:conformsTo from conforms_to
        self.modify_conforms_to(dataset_dict, dataset_ref)
        # foaf:page from documentation
        self.modify_documentation(dataset_dict, dataset_ref)
        # dct:accrualPeriodicity from frequency
        self.modify_frequency(dataset_dict, dataset_ref)
        # dct:hasVersion from has_version
        self.modify_has_version(dataset_dict, dataset_ref)
        # dct:identifier from uri (dcat plugin)
        # dct:isReferencedBy from referenced_by
        self.add_referenced_by(dataset_dict, dataset_ref)

        # dct:isVersionOf from is_version_of (dcat plugin)
        # dcat:landingPage
        self.add_landing_page(dataset_dict, dataset_ref)
        # dct:language 
        self.modify_languages(dataset_dict, dataset_ref)
        # adms:identifier from alternate_identifier
        self.modify_alternate_identifier(dataset_dict, dataset_ref)
        # dct:provenance from provenance
        # dct:relation
        self.add_relations(dataset_dict, dataset_ref)
        # dct:issued from (dcat plugin)
        # dct: from source
        self.modify_source(dataset_dict, dataset_ref)
        # dcat:spatialResolutionInMeters
        self.add_spatial_resolution_in_meters(dataset_dict, dataset_ref)
        # dcat:temporalResolution
        self.add_temporal_resolution(dataset_dict, dataset_ref)
        # dct:type
        self.modify_type(dataset_dict, dataset_ref)
        # dct:modified from modified (dcat plugin)
        # owl:versionInfo from version (dcat plugin)
        # adms:versionNotes from version_notes (dcat plugin)

        # Distributions from resources

        # dcat:accessURL (dcat plugin)
        # dct:title (dcat plugin)
        # dct:description (dcat plugin)
        # dcatap:availability skos:Concept Ajánlott 1 Elérhetőség DCAT Availability
        self.add_availability(dataset_dict, dataset_ref)
        # dct:format
        self.modify_format(dataset_dict, dataset_ref)
        # dct:license dct:LicenseDocument Kötelező 1 Licenc Creative Commons Licenses
        # dcat:accessService dcat:DataService Opcionális API hozzáférés DataService metaadat rekord URL, amelyen keresztül az adat elérhető
        self.add_access_service(dataset_dict, dataset_ref)
        # dcat:byteSize xsd:decimal Opcionális 1 Fájlméret bájtok száma API esetén nincs értelme
        # dcat:compressFormat dct:MediaType Opcionális 1 Tömörítési formátum IANA Media Types (MIME types)
        # self.add_compress_format(dataset_dict, dataset_ref)
        # foaf:page foaf:Document Opcionális Dokumentáció URL Az egyszerűség kedvéért az adatelérés dokumentációjára mutató URL-t kérünk
        self.add_resource_documentation(dataset_dict, dataset_ref)
        # dcat:downloadURL rdfs:Resource Opcionális Letöltési link URL Közvetlenül a letölthető fájlra mutató link
        # dct:language dct:LinguisticSystem Ajánlott Nyelvek EU Vocabuaries Language Az adat milyen nyelveken érhető el.
        self.add_resource_languages(dataset_dict, dataset_ref)
        # dct:conformsTo dct:Standard Opcionális Megfelelés Szabvány, előírás URL Milyen szabványok, előírások alapján készült ez az adatelérés
        self.add_resource_conforms_to(dataset_dict, dataset_ref)
        # dcat:mediaType dct:MediaType Ajánlott 1 Formátum IANA Media Types (MIME types)
        self.modify_media_type(dataset_dict, dataset_ref)
        # dcat:packageFormat dct:MediaType Opcionális 1 Csomagolási formátum
        # self.add_package_format(dataset_dict, dataset_ref)
        # dct:issued xsd:date or xsd:dateTime Opcionális 1 Közzététel dátuma
        # dct:rights dct:RightsStatement Opcionális 1 Jognyilatkozat Jognyilatkozat URL Ezen adateléréssel kapcsolatos jogok leírására mutató URL. Lehet IPR is. Licencet nem itt kell megadni.
        self.modify_resource_rights(dataset_dict, dataset_ref)
        # dcat:spatialResolutionInMeters xsd:decimal Opcionális Térbeli felbontás Szám, méterben megadva A legnagyobb elérhető felbontás
        self.add_resource_spatial_resolution_in_meters(dataset_dict, dataset_ref)
        # dcat:temporalResolution xsd:duration Opcionális Időbeli felbontás xsd:duration A legkisebb beazonosítható időegység az adatokban
        self.add_resource_temporal_resolution(dataset_dict, dataset_ref)
        # adms:status skos:Concept Opcionális 1 Státusz Ezek egyike: Completed, Deprecated, Under Development, Withdrawn ADMS Status szókészlet (befejezett, elavult, fejlesztés alatt, visszavont),
        self.add_resource_status(dataset_dict, dataset_ref)
        # dct:modified xsd:date or xsd:dateTime Opcionális 1 Utolsó módosítás ideje

    def add_themes_from_groups(self, dataset_dict, dataset_ref):
        groups = self._get_dict_value(dataset_dict, 'groups')

        self.g.remove((dataset_ref, DCAT.theme, None))

        group_show = logic.get_action('group_show')
        if groups:
            translations = self._get_translations_for_terms([g['title'] for g in groups] )

            for group in groups:
                try:
                    group_dict = group_show({'ignore_auth': True},
                                        {'id': group['id'],
                                        'include_datasets': False,
                                        'include_tags': False,
                                        'include_users': False,
                                        'include_groups': False,
                                        'include_extras': True,
                                        'include_followers': False}
                                        )
                except Exception as err:
                    log.warning("Cannot get group for %s: %s", group['id'], err, exc_info=err)

                theme_name = group_dict.get('title')
                schema_url = group_dict.get('schema_url')
                theme_ref = URIRef(schema_url)
                self.g.add((dataset_ref, DCAT.theme, theme_ref))

                concept = URIRef(schema_url)
                self.g.add((concept, RDF['type'], SKOS.Concept))
                for lang, translation in translations[group['title']].items():
                    self.g.add((concept, SKOS.prefLabel, Literal(translation, lang=lang)))
                
                self.g.add((concept, SKOS.prefLabel, Literal(theme_name, lang=hu_lang)))

        else:
            schema_url = THEME_BASE_URI + DEFAULT_THEME_KEY
            theme_ref = URIRef(schema_url)
            self.g.add((dataset_ref, DCAT.theme, theme_ref))
            concept = URIRef(schema_url)
            self.g.add((concept, RDF['type'], SKOS.Concept))

    def modify_keywords(self, dataset_dict, dataset_ref):
        field_value_arr = self._get_dict_value(dataset_dict, 'tags')
        if field_value_arr:
            self.g.remove((dataset_ref, DCAT.keyword, None))
            
            for field_value in field_value_arr:
                name = field_value['name']
                localizedData = self._get_localized_tag_for_value(name, 'eurovoc')
                if localizedData:
                    concept = URIRef(localizedData['url'])
                    self.g.add((dataset_ref, DCAT.keyword, concept))
                    for lang, translation in localizedData['translations'].items():
                        self.g.add((concept, SKOS.prefLabel, Literal(translation, lang=lang)))

    def modify_languages(self, dataset_dict, dataset_ref):
        self._create_node_from_multiselect(dataset_dict, dataset_ref, 'language', DCT.language, 'languages', DCT.LinguisticSystem)

    def modify_spatial(self, dataset_dict, dataset_ref):
        self._create_node_from_multiselect(dataset_dict, dataset_ref, 'spatial_uri', DCT.spatial, 'spatials', DCT.Location)

    def modify_conforms_to(self, dataset_dict, dataset_ref):
        self._create_node_from_multilist(dataset_dict, dataset_ref, 'conforms_to', DCT.conformsTo, DCT.Standard)

    def modify_documentation(self, dataset_dict, dataset_ref):
        self._create_node_from_multilist(dataset_dict, dataset_ref, 'documentation', FOAF.page, FOAF.Document)

    def modify_has_version(self, dataset_dict, dataset_ref):
        self._create_node_from_multilist(dataset_dict, dataset_ref, 'has_version', DCT.hasVersion, DCT.Dataset)
    
    def modify_alternate_identifier(self, dataset_dict, dataset_ref):
        self._create_node_from_multilist(dataset_dict, dataset_ref, 'alternate_identifier', ADMS.identifier, ADMS.Identifier)

    
    def modify_source(self, dataset_dict, dataset_ref):
        self._create_node_from_multilist(dataset_dict, dataset_ref, 'source', DCT.source, DCT.Dataset)

    def add_resource_conforms_to(self, dataset_dict, dataset_ref):
        for resource_dict in dataset_dict.get('resources', []):
            distribution = URIRef(resource_uri(resource_dict))
            self._create_node_from_multilist(resource_dict, distribution, 'conforms_to', DCT.conformsTo, DCT.Standard)

    def add_availability(self, dataset_dict, dataset_ref):
        for resource_dict in dataset_dict.get('resources', []):
            distribution = URIRef(resource_uri(resource_dict))
            self._create_node_from_select(resource_dict, distribution, 'availability', DCATAP.availability, 'availability', SKOS.Concept)

    def add_access_service(self, dataset_dict, dataset_ref):
        for resource_dict in dataset_dict.get('resources', []):
            distribution = URIRef(resource_uri(resource_dict))
            self._create_node_from_multilist(resource_dict, distribution, 'access_service', DCAT.accessService, DCAT.DataService)

    def add_resource_languages(self, dataset_dict, dataset_ref):
        for resource_dict in dataset_dict.get('resources', []):
            distribution = URIRef(resource_uri(resource_dict))
            self._create_node_from_multiselect(resource_dict, distribution, 'language', DCT.language, 'languages', DCT.LinguisticSystem)

    def add_compress_format(self, dataset_dict, dataset_ref):
        for resource_dict in dataset_dict.get('resources', []):
            distribution = URIRef(resource_uri(resource_dict))
            self._create_node_from_select(resource_dict, distribution, 'compress_format', DCAT.compressFormat, 'mimetypes', DCT.MediaType)

    def add_package_format(self, dataset_dict, dataset_ref):
        for resource_dict in dataset_dict.get('resources', []):
            distribution = URIRef(resource_uri(resource_dict))
            self._create_node_from_select(resource_dict, distribution, 'package_format', DCAT.packageFormat, 'mimetypes', DCT.MediaType)

    def add_resource_documentation(self, dataset_dict, dataset_ref):
        for resource_dict in dataset_dict.get('resources', []):
            distribution = URIRef(resource_uri(resource_dict))
            self._create_node_from_multilist(resource_dict, distribution, 'documentation', FOAF.page, FOAF.Document)

    def add_resource_status(self, dataset_dict, dataset_ref):
        for resource_dict in dataset_dict.get('resources', []):
            distribution = URIRef(resource_uri(resource_dict))
            self._create_node_from_select(resource_dict, distribution, 'status', ADMS.status, 'adms_statuses', SKOS.Concept)

    def modify_resource_rights(self, dataset_dict, dataset_ref):
        for resource_dict in dataset_dict.get('resources', []):
            distribution = URIRef(resource_uri(resource_dict))
            self.g.remove( (distribution, DCT.rights, None) )
            if self.has_value_for(resource_dict, 'rights'):
                new_ref = URIRef(resource_dict['rights'])
                concept = URIRef(resource_dict['rights'])
                self.g.add((concept, RDF['type'], DCT.RightsStatement))
                self.g.add((distribution, DCT.rights, new_ref))

    def modify_frequency(self, dataset_dict, dataset_ref):
        self._create_node_from_select(dataset_dict, dataset_ref, 'frequency', DCT.accrualPeriodicity, 'frequencies', DCT.Frequency)

    def modify_access_rights(self, dataset_dict, dataset_ref):
        self._create_node_from_select(dataset_dict, dataset_ref, 'access_rights', DCT.accessRights, 'access-rights', DCT.RightsStatement)

    def modify_type(self, dataset_dict, dataset_ref):
        self._create_node_from_select(dataset_dict, dataset_ref, 'dcat_type', DCT.type, 'dataset-types', SKOS.Concept)

    def _get_localized_tag_for_value(self, value, vocabulary_id):
        tag_show = toolkit.get_action('tag_show')
        try:
            tag = tag_show(data_dict={'id': value,'vocabulary_id': vocabulary_id})
            url = HutemplateTagVocabulary.by_tag_id(tag['id']).url
            translation_map = self._get_translations_for_terms([value])
            return {
                'url': url,
                'translations': translation_map[value]
            }
        except:
            return None

    def _get_translations_for_terms(self, terms):
        translations = logic.action.get.term_translation_show({'model': model},{'terms': terms})
        translation_map = {}
        for t in translations:
            if t['term'] not in translation_map:
                translation_map[t['term']] = {}
            translation_map[t['term']][t['lang_code']] = t['term_translation']
        return translation_map

    def modify_format(self, dataset_dict, dataset_ref):
        format_data = self.load_format_data()
        for resource_dict in dataset_dict.get('resources', []):
            distribution = URIRef(resource_uri(resource_dict))
            self.g.remove((distribution, DCT['format'], None))
            guessed_format = guess_format(resource_dict, format_data)
            if guessed_format:
                new_ref = URIRef(guessed_format.url)
                concept = URIRef(guessed_format.url)
            else:
                new_ref = URIRef(FORMAT_BASE_URI + DEFAULT_FORMAT_CODE)
                concept = URIRef(FORMAT_BASE_URI + DEFAULT_FORMAT_CODE)

            self.g.add((concept, RDF['type'], DCT.MediaTypeOrExtent))
            self.g.add((concept, RDF['type'], DCT.FileFormat))
            self.g.add((distribution, DCT['format'], new_ref))

    def modify_media_type(self, dataset_dict, dataset_ref):
        for resource_dict in dataset_dict.get('resources', []):
            distribution = URIRef(resource_uri(resource_dict))
            if 'mimetype' in resource_dict and resource_dict['mimetype'] is not None :
                self.g.remove((distribution, DCAT['mediaType'], None))
                new_ref = URIRef(MEDIA_TYPE_BASE_URI + resource_dict['mimetype'])
                concept = URIRef(MEDIA_TYPE_BASE_URI + resource_dict['mimetype'])
                self.g.add((concept, RDF['type'], DCT.MediaType))
                self.g.add((distribution, DCAT['mediaType'], new_ref))

    def add_resource_spatial_resolution_in_meters(self, dataset_dict, dataset_ref):
        for resource_dict in dataset_dict.get('resources', []):
            distribution = URIRef(resource_uri(resource_dict))
            self.add_spatial_resolution_in_meters(resource_dict, distribution)

    def add_spatial_resolution_in_meters(self, dataset_dict, dataset_ref):
        g = self.g
        if self.has_value_for(dataset_dict, 'spatial_resolution_in_meters'):
            try:
                g.add( (dataset_ref, DCAT.spatialResolutionInMeters, Literal(float(dataset_dict.get('spatial_resolution_in_meters')), datatype=XSD.decimal)) )
            except:
                return

    def add_resource_temporal_resolution(self, dataset_dict, dataset_ref):
        for resource_dict in dataset_dict.get('resources', []):
            distribution = URIRef(resource_uri(resource_dict))
            self.add_temporal_resolution(resource_dict, distribution)

    def add_temporal_resolution(self, dataset_dict, dataset_ref):
        g = self.g
        temporal_resolution = self._get_dict_value(dataset_dict, 'temporal_resolution')
        if temporal_resolution:
            tr_string = {
                'SEC': 'PT1S',
                'MIN': 'PT1M',
                'HOUR': 'PT1H',
                'DAY': 'P1D',
                'WEEK': 'P7D',
                'MONTH': 'P1M',
                'QUARTER': 'P3M',
                'YEAR_HALF': 'P6M',
                'YEAR': 'P1Y'
            }.get(temporal_resolution, None)
            if tr_string:
                g.add( (dataset_ref, DCAT.temporalResolution, Literal(tr_string, datatype=XSD.duration)) )

    def add_relations(self, dataset_dict, dataset_ref):
        g = self.g
        if self.has_value_for(dataset_dict, 'relations'):
            for rel in dataset_dict.get('relations'):
                g.add( (dataset_ref, DCT.relation, URIRef(rel)) )

    def add_referenced_by(self, dataset_dict, dataset_ref):
        g = self.g
        if self.has_value_for(dataset_dict, 'referenced_by'):
            g.add( (dataset_ref, DCT.isReferencedBy, URIRef(dataset_dict.get('referenced_by'))) )

    def add_landing_page(self, dataset_dict, dataset_ref):
        g = self.g
        g.remove( (dataset_ref, DCAT.landingPage, None) )
        if self.has_value_for(dataset_dict, 'landing_page'):
            field_value = dataset_dict.get('landing_page')
            new_ref = Literal(field_value)
            if _is_valid_uri(field_value):
                new_ref = URIRef(field_value)
            
            concept = Literal(field_value)
            if _is_valid_uri(field_value):
                concept = URIRef(field_value)

            self.g.add((dataset_ref, DCAT.landingPage, new_ref))
            self.g.add((concept, RDF['type'], FOAF.Document))

    def add_contact_point(self, dataset_dict, dataset_ref):
        g = self.g
        g.remove( (dataset_ref, DCAT.contactPoint, None) )
        if self.has_value_for(dataset_dict, 'maintainer') or self.has_value_for(dataset_dict, 'maintainer_email'):
            contactPoint = BNode()
            g.add( (dataset_ref, DCAT.contactPoint, contactPoint) )
            if self.has_value_for(dataset_dict, 'maintainer'):
                g.add( (contactPoint, VCARD.fn, Literal(dataset_dict.get('maintainer'))) )
            if self.has_value_for(dataset_dict, 'maintainer_email'):
                g.add( (contactPoint, VCARD.hasEmail, URIRef(dataset_dict.get('maintainer_email'))) )
            g.add( (contactPoint, RDF.type, VCARD.Kind) )

    def add_creator(self, dataset_dict, dataset_ref):
        g = self.g
        g.remove( (dataset_ref, DCT.creator, None) )
        if self.has_value_for(dataset_dict, 'author') or self.has_value_for(dataset_dict, 'author_email'):
            contactPoint = BNode()
            g.add( (dataset_ref, DCT.creator, contactPoint) )
            g.add( (contactPoint, RDF.type, FOAF.Agent) )
            if self.has_value_for(dataset_dict, 'author'):
                g.add( (contactPoint, FOAF.name, Literal(dataset_dict.get('author'))) )
            if self.has_value_for(dataset_dict, 'author_email'):
                g.add( (contactPoint, FOAF.mbox, URIRef("mailto:"+dataset_dict.get('author_email'))) )

    def add_publisher_extra(self, dataset_dict, dataset_ref):
        g = self.g
        org_id = dataset_dict.get('owner_org')
        org_show = logic.get_action('organization_show')
        if org_id:
            try:
                org_dict = org_show({'ignore_auth': True},
                                    {'id': org_id,
                                     'include_datasets': False,
                                     'include_tags': False,
                                     'include_users': False,
                                     'include_groups': False,
                                     'include_extras': True,
                                     'include_followers': False}
                                    )
            except Exception as err:
                log.warning("Cannot get org for %s: %s", org_id, err, exc_info=err)

        # find the publisher node
        for s,p,o in g.triples( (dataset_ref, DCT.publisher, None) ):
            #add the email
            g.add( (o, RDF['type'], FOAF.Organization) )
            g.add( (o, RDF['type'], FOAF.Agent) )
            if self.has_value_for(org_dict, 'email'):
                g.add( (o, FOAF.mbox, URIRef("mailto:"+org_dict.get('email'))) )
            if self.has_value_for(org_dict, 'homepage'):
                g.add( (o, FOAF.homepage, URIRef(org_dict.get('homepage'))) )

    def load_format_data(self):
        user = toolkit.get_action('get_site_user')({'ignore_auth': True}, {})
        context = {'user': user['name']}
        try:
            data = {'id': 'file-types'}
            vocab = toolkit.get_action('vocabulary_show')(context, data)
        except toolkit.ObjectNotFound:
            return []
        return HutemplateTagVocabulary.all_by_vocabulary_id(vocab['id'])

    def _create_node_from_multilist(self, dataset_dict, dataset_ref, filed_name, node_type, rdf_type):
        field_value_arr = self._get_dict_value(dataset_dict, filed_name)
        if field_value_arr:
            self.g.remove((dataset_ref, node_type, None))
            for field_value in field_value_arr:
                new_ref = Literal(field_value)
                if _is_valid_uri(field_value):
                    new_ref = URIRef(field_value)
                
                concept = Literal(field_value)
                if _is_valid_uri(field_value):
                    concept = URIRef(field_value)

                self.g.add((dataset_ref, node_type, new_ref))
                self.g.add((concept, RDF['type'], rdf_type))
    
    def _create_node_from_multiselect(self, dataset_dict, dataset_ref, filed_name, node_type, vocabulary_name, rdf_type):
        field_value = self._get_dict_value(dataset_dict, filed_name)
        if field_value:
            self.g.remove((dataset_ref, node_type, None))
            for v in field_value.split(','):
                v = v.replace('{','').replace('}','')
                localizedData = self._get_localized_tag_for_value(v, vocabulary_name)
                if localizedData:
                    concept = URIRef(localizedData['url'])
                    self.g.add((dataset_ref, node_type, concept))
                    self.g.add((concept, RDF['type'], rdf_type))
                    for lang, translation in localizedData['translations'].items():
                        self.g.add((concept, SKOS.prefLabel, Literal(translation, lang=lang)))

    def _create_node_from_select(self, dataset_dict, dataset_ref, filed_name, node_type, vocabulary_name, rdf_type):
        field_value = self._get_dict_value(dataset_dict, filed_name)
        if field_value:
            self.g.remove((dataset_ref, node_type, None))
            localizedData = self._get_localized_tag_for_value(field_value, vocabulary_name)
            if localizedData:
                new_ref = URIRef(localizedData['url'])
                concept = URIRef(localizedData['url'])

                self.g.add((dataset_ref, node_type, new_ref))
                self.g.add((concept, RDF['type'], rdf_type))
                for lang, translation in localizedData['translations'].items():
                    self.g.add((concept, SKOS.prefLabel, Literal(translation, lang=lang)))

    def has_value_for(self, dataset_dict, key):
        return key in dataset_dict.keys() and dataset_dict.get(key)

    def _add_uri_node(self, _dict, ref, item, base_uri=''):

        key, pred, fallback, _type = item

        value = self._get_dict_value(_dict, key)
        if value:
            self.g.add((ref, pred, _type(base_uri + value)))
            return True
        elif fallback:
            self.g.add((ref, pred, _type(base_uri + fallback)))
            return False
        else:
            return False

    def _remove_node(self, _dict, ref, item):

        key, pred, fallback, _type = item

        value = self._get_dict_value(_dict, key)
        if value:
            self.g.remove((ref, pred, _type(value)))


def guess_format(resource_dict, format_data):
    f = resource_dict.get('format')

    if not f:
        log.info('No format found')
        return None
    format_mapping = {}
    for format in format_data:
        format_mapping[format.tag_name.lower()] = format
    ret = format_mapping.get(f.lower(), None)

    if not ret:
        log.info('Mapping not found for format %s', f)

    return ret

_invalid_uri_chars = '<>" {}|\\^`'
def _is_valid_uri(uri):
    for c in _invalid_uri_chars:
        if c in uri: return False
    return True