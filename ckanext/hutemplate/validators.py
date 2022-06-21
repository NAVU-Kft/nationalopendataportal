import logging
import ckan.plugins as p
import ckan.lib.navl.dictization_functions as df
from ckanext.pages import db
from ckanext.scheming.validation import scheming_validator, register_validator
import json
from itertools import count

missing = df.missing
StopOnError = df.StopOnError
Invalid = df.Invalid

log = logging.getLogger(__name__)

def not_empty_if_blog(key, data, errors, context):
    value = data.get(key)
    if data.get(('page_type',), '') == 'blog':
        if value is df.missing or not value:
            if key == 'blog_type':
                errors[key].append('Blog type must be supplied')
            else:
                errors[key].append(key+' Must be supplied')

def not_empty_if_page(key, data, errors, context):
    value = data.get(key)
    if data.get(('page_type',), '') != 'blog':
        if value is df.missing or not value:
            if key == 'page_subtype':
                errors[key].append('Page type must be supplied')
            else:
                errors[key].append(key+' Must be supplied')

def page_subtype_is_unique(key, data, errors, context):
    if data.get(('page_type',), '') == 'blog':
        return
    
    value = data.get(key)
    if value is not df.missing and value:
        session = context['session']
        page = context.get('page')
        query = session.query(db.Page).filter(db.Page.name!=page)
        result = query.all()
        for page in result:
            ext = json.loads(page.extras)
            if type and ext['page_subtype'] == value:
                errors[key].append(p.toolkit._('Page type already exists in database'))

def not_empty_tags(key, data, errors, context):
    value = data.get(('tags',0,'name'))
    log.info("tags: "+str(value))
    value2 = data.get(('tag_string',))
    log.info("tag_string: "+str(value2))
    if (not value or value is missing) and (not value2 or value2 is missing):
        errors[key].append(p.toolkit._('Missing value'))
        raise StopOnError

@scheming_validator
@register_validator
def vocabulary_validator(field, schema):
    def validator(key, data, errors, context):
        value = data.get(key)
        vocabulary = field.get('vocabulary')
        model = context['model']
        session = context['session']
        if value and vocabulary:
            query1 = session.query(model.Vocabulary.id).filter_by(name=vocabulary)
            vocabulary_id = query1.first()
            query = session.query(model.Tag)\
                .filter(model.Tag.vocabulary_id==vocabulary_id)\
                .filter(model.Tag.name==value)\
                .count()
            if not query:
                errors[key].append(p.toolkit._('Tag %s does not belong to vocabulary %s') % (value, vocabulary))
                raise StopOnError

    return validator

@scheming_validator
@register_validator
def eurovoc_tags_validator(field, schema):
    def validator(_key, data, errors, context):
        tag_names = []
        for key in data.keys():
            if key[0] == 'tags' and key[2] == 'name':
                tag_names.append(data.get(key))
        
        vocabulary = 'eurovoc'
        model = context['model']
        session = context['session']
        for value in tag_names:
            if value and vocabulary:
                query1 = session.query(model.Vocabulary.id).filter_by(name=vocabulary)
                vocabulary_id = query1.first()
                query = session.query(model.Tag)\
                    .filter(model.Tag.vocabulary_id==vocabulary_id)\
                    .filter(model.Tag.name==value)\
                    .count()
                if not query:
                    errors['tags'].append(p.toolkit._('Tag %s does not belong to vocabulary %s') % (value, vocabulary))

        
    return validator

@scheming_validator
@register_validator
def group_required_validator(field, schema):
    def validator(_key, data, errors, context):
        group_ids = []
        for key in data.keys():
            if key[0] == 'groups' and key[2] == 'id':
                group_ids.append(data.get(key))
        
        if len(group_ids) <= 0:
            errors[('groups__0__id',)].append(p.toolkit._('Missing value'))

    return validator

@scheming_validator
@register_validator
def vocabulary_multiple_validator(field, schema):
    def validator(key, data, errors, context):
        value_str = data.get(key)
        values = value_str.split(',')
        vocabulary = field.get('vocabulary')
        model = context['model']
        session = context['session']
        for value in values:
            if value and vocabulary:
                query1 = session.query(model.Vocabulary.id).filter_by(name=vocabulary)
                vocabulary_id = query1.first()
                query = session.query(model.Tag)\
                    .filter(model.Tag.vocabulary_id==vocabulary_id)\
                    .filter(model.Tag.name==value)\
                    .count()
                if not query:
                    errors[key].append(p.toolkit._('Tag %s does not belong to vocabulary %s') % (value, vocabulary))

    return validator