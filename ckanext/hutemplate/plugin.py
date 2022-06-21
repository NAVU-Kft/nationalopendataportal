import logging
import datetime
import six
from datetime import date
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultTranslation
import ckan.lib.helpers as h
from ckanext.pages.interfaces import IPagesSchema
from ckan.common import _, c, ungettext
from ckanext.hutemplate.validators import not_empty_if_page, not_empty_if_blog, page_subtype_is_unique, not_empty_tags, vocabulary_validator
from ckanext.hutemplate.HTMLFirstLink import HTMLFirstLink
from flask import Blueprint
from ckan.common import config, request, is_flask_request
from ckanext.hutemplate.controllers.registerRoutes import registerRoutes
from ckanext.hutemplate.commands.hutemplate import hutemplate
from ckanext.multilingual.plugin import translate_data_dict
from ckan.lib.helpers import build_nav_main as core_build_nav_main
from ckanext.hutemplate.model.blog_types import blog_t, get_blog_type_record
from ckanext.hutemplate.model.page_types import page_t, get_page_type_record
from collections import OrderedDict

from ckanext.hutemplate.logic.excel_logic import hutemplate_export_excel, hutemplate_auth


log = logging.getLogger(__name__)

def get_page_for_type(type=None):
    page_list = toolkit.get_action('ckanext_pages_list')(
        None, {'private': False, 'page_type': 'page'})
    
    for page in page_list:
        if type and page['page_subtype'] == type:
            return page

    return None

def vocabulary_choices(field):
    vocabulary_id = field['vocabulary']
    try:
        tag_list = toolkit.get_action('tag_list')
        tags = tag_list(data_dict={'vocabulary_id': vocabulary_id})
        translated = translateArray(tags)
        return [{ 'value': key, 'label': value } for key, value in translated.items()]
    except toolkit.ObjectNotFound:
        return []

def translateArray(arr):
    dict = {}
    for el in arr:
        dict[el] = el
    return translate_data_dict(dict)

def blog_types():
    return blog_t()

def blog_name_from_id(category_name_or_id):
    record = get_blog_type_record(category_name_or_id)
    if record is None:
        return None
    return record['label']

def page_types():
    return page_t()

def page_name_from_id(category_name_or_id):
    record = get_page_type_record(category_name_or_id)
    if record is None:
        return None
    return record['label']
    
def mapToSelect(arr, default=None):
    mapped = []
    if default:
        mapped.append(dict(text=default, value=''))
    for item in arr:
        mapped.append(dict(text=item['label'], value=item['key']))
    return mapped

def get_recent_blog_posts_by_type(number=5, type=None, exclude=None):
    blog_list = toolkit.get_action('ckanext_pages_list')(
        None, {'order_publish_date': True, 'private': False,
               'page_type': 'blog'}
    )
    new_list = []
    for blog in blog_list:
        if exclude and blog['name'] == exclude:
            continue
        if type and blog['blog_type'] != type:
            continue
        new_list.append(blog)
        if len(new_list) == number:
            break

    return new_list

def get_company_settings():
    return {
        'company_name' : config.get('ckanext.hutemplate.company_name', ''),
        'company_address' : config.get('ckanext.hutemplate.company_address', ''),
        'company_phone' : config.get('ckanext.hutemplate.company_phone', ''),
        'company_email' : config.get('ckanext.hutemplate.company_email', ''),
        'company_longitude' : config.get('ckanext.hutemplate.company_longitude', ''),
        'company_latitude' : config.get('ckanext.hutemplate.company_latitude', '')
    }

def get_github_url():
    return config.get('ckanext.hutemplate.github_url', '')

def get_download_total(pkg):
    download_num = 0
    for resource in pkg['resources']:
        download_num = download_num + resource['tracking_summary']['total']
    return download_num

def monogram(user_name):
    words = user_name.split()
    if len(words) > 1:
        mg = ""
        for word in user_name.split():
            mg += word[0:1]
        return mg
    if len(words) == 1:
        return user_name[0:2]
    
    
def user_create(context, data_dict=None):
    if c.userobj:
        return {'success': True}
    else:
        return {'success': False,
                'msg': 'Only members can invite'}

def now():
    return datetime.datetime.now().strftime('%Y-%m-%d')

def login_handler():
    came_from = request.params.get(u'came_from')
    if not came_from:
        came_from = h.url_for(u'user.logged_in')
    handler = getattr(request.environ[u'repoze.who.plugins'][u'friendlyform'], u'login_handler_path')
    return h.url_for(handler, came_from=came_from)

def blog_link(post):
    parser = HTMLFirstLink()
    parser.feed(post['content'])
    return {'link': parser.link, 'target': parser.target}

def get_url_param(key):
    params_items = request.params.items(multi=True) if is_flask_request() else request.params.items()
    params = list(params_items)
    filtered = list(filter(lambda c: c[0] == key, params))
    if(len(filtered) > 0):
        return filtered[0][1]
    return None

def is_string(value):
    return isinstance(value, six.string_types)
class HutemplatePlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm, DefaultTranslation):
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(IPagesSchema)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IClick)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IValidators)
    plugins.implements(plugins.IAuthenticator)
    plugins.implements(plugins.IFacets, inherit=True)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IActions)
    
    # IClick
    def get_commands(self):
        return [hutemplate]

    

    def get_helpers(self):
        return {
            'build_nav_main': core_build_nav_main, #override the pages nav_main func, to the default one
            'get_recent_blog_posts_by_type': get_recent_blog_posts_by_type,
            'mapToSelect': mapToSelect,
            'get_page_for_type': get_page_for_type,
            'blog_types': blog_types,
            'blog_name_from_id': blog_name_from_id,
            'page_types': page_types,
            'page_name_from_id': page_name_from_id,
            'vocabulary_choices': vocabulary_choices,
            'get_company_settings': get_company_settings,
            'get_github_url': get_github_url,
            'get_download_total': get_download_total,
            'monogram': monogram,
            'now': now,
            'login_handler': login_handler,
            'blog_link': blog_link,
            'get_url_param': get_url_param,
            'is_string': is_string
        }
        

    #IPagesSchema
    def update_pages_schema(self, schema):
        schema.update({
            'blog_type': [not_empty_if_blog],
            'page_subtype': [page_subtype_is_unique]
            })
        return schema

    #IAuthFunctions
    def get_auth_functions(self):
        return {
            'user_create': user_create,
            'hutemplate_export_excel': hutemplate_auth}
    
    # IActions
    def get_actions(self):
        return {
            'hutemplate_export_excel': hutemplate_export_excel
        }

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('assets', 'hutemplate')

    def create_package_schema(self):
        schema = super(HutemplatePlugin, self).create_package_schema()
        return schema

    def update_package_schema(self):
        schema = super(HutemplatePlugin, self).update_package_schema()
        return schema

    def show_package_schema(self):
        schema = super(HutemplatePlugin, self).show_package_schema()
        return schema

    def update_config_schema(self, schema):
        ignore_missing = toolkit.get_validator('ignore_missing')
        schema.update({
            # This is an existing CKAN core configuration option, we are just
            # making it available to be editable at runtime
            'ckanext.hutemplate.company_name': [ignore_missing],
            'ckanext.hutemplate.company_address': [ignore_missing],
            'ckanext.hutemplate.company_phone': [ignore_missing],
            'ckanext.hutemplate.company_email': [ignore_missing],
            'ckanext.hutemplate.company_longitude': [ignore_missing],
            'ckanext.hutemplate.company_latitude': [ignore_missing],
        })
        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    # IBlueprint
    def get_blueprint(self):
        u'''Return a Flask Blueprint object to be registered by the app.'''

        # Create Blueprint for plugin
        blueprint = Blueprint(self.name, self.__module__)
        blueprint.template_folder = u'templates'
        registerRoutes(blueprint)

        return blueprint

    # IValidators
    def get_validators(self):
        return {
            'not_empty_tags': not_empty_tags
        }

    # IFacets
    def dataset_facets(self, facets_dict, package_type):
        final_dict = OrderedDict()
        final_dict['organization'] = facets_dict['organization']
        final_dict['groups'] = facets_dict['groups']
        final_dict['temporal_start'] = _('Temporal coverage')
        final_dict['tags'] = facets_dict['tags']
        final_dict['res_format'] = facets_dict['res_format']
        final_dict['license_id'] = facets_dict['license_id']

        return final_dict

    # IPackageController
    def before_search(self, search_params):
        extras = search_params.get('extras')
        if not extras:
            # There are no extras in the search params, so do nothing.
            return search_params

        temporal_start = extras.get('ext_temporal_start')
        temporal_end = extras.get('ext_temporal_end')

        if not temporal_start and not temporal_end:
            # The user didn't select either a start and/or end date, so do nothing.
            return search_params

        fq = search_params.get('fq', '')
        #(StartA <= EndB) and (EndA >= StartB)
        end = ''
        if temporal_start:
            now_str = date.today()
            end = 'extras_temporal_end:[{sd}T00:00:00Z TO {now}T00:00:00Z]'.format(sd=temporal_start, now=now_str)

        start = ''
        if temporal_end:
            start = 'extras_temporal_start:[1000-01-01T00:00:00Z TO {ed}T00:00:00Z]'.format(ed=temporal_end)

        fq = '{fq} {start} {end}'.format(fq=fq, end=end, start=start)
        log.info(str(fq))
        search_params['fq'] = fq

        return search_params

    # IAuthenticator
    def identify(self):
        return None

    def login(self):
        return None

    def logout(self):
        h.flash_success(_("You are now logged out."))
        return None