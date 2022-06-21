import logging

from sqlalchemy import types, Column, Table, ForeignKey

from ckan.model import Session
from ckan.model import meta
from ckan.model.domain_object import DomainObject


log = logging.getLogger(__name__)

__all__ = ['HutemplateTagVocabulary', 'hutemplate_tag_table', 'setup']

hutemplate_tag_table = Table('hutemplate_tag', meta.metadata,
    Column('id', types.Integer, primary_key=True),
    Column('vocabulary_id', types.UnicodeText, ForeignKey("vocabulary.id", ondelete="CASCADE"), nullable=False),
    Column('tag_id', types.UnicodeText, ForeignKey("tag.id", ondelete="CASCADE"), nullable=False),
    Column('tag_name', types.UnicodeText, nullable=False, index=True),
    Column('url', types.UnicodeText, nullable=False))


def setup():
    #Setting up tag multilang table
    if not hutemplate_tag_table.exists():
        try:
            hutemplate_tag_table.create()
        except Exception as e:
            # Make sure the table does not remain incorrectly created
            if hutemplate_tag_table.exists():
                Session.execute('DROP TABLE hutemplate_tag')
                Session.commit()

            raise e

        log.info('hutemplate Tag Vocabulary table created')
    else:
        log.info('hutemplate Tag Vocabulary table already exist')


class HutemplateTagVocabulary(DomainObject):
    def __init__(self, tag_id=None, vocabulary_id=None, tag_name=None, url=None):
        self.tag_id = tag_id
        self.tag_name = tag_name
        self.url = url
        self.vocabulary_id = vocabulary_id

    @classmethod
    def all_by_vocabulary_id(self, vocabulary_id, autoflush=True):
        query = meta.Session.query(HutemplateTagVocabulary).filter(HutemplateTagVocabulary.vocabulary_id==vocabulary_id)
        query = query.autoflush(autoflush)
        tag = query.all()
        return tag

    @classmethod
    def by_name(self, tag_name, autoflush=True):
        query = meta.Session.query(HutemplateTagVocabulary).filter(HutemplateTagVocabulary.tag_name==tag_name)
        query = query.autoflush(autoflush)
        tag = query.first()
        return tag

    @classmethod
    def by_url(self, tag_url, autoflush=True):
        query = meta.Session.query(HutemplateTagVocabulary).filter(HutemplateTagVocabulary.url==tag_url)
        query = query.autoflush(autoflush)
        tag = query.first()
        return tag

    @classmethod
    def by_tag_id(self, tag_id, autoflush=True):
        query = meta.Session.query(HutemplateTagVocabulary).filter(HutemplateTagVocabulary.tag_id==tag_id)
        query = query.autoflush(autoflush)
        tag = query.first()
        return tag

    def persist(self):
        session = meta.Session
        try:
            session.add_all([self])
            session.commit()
        except Exception as e:
            # on rollback, the same closure of state
            # as that of commit proceeds. 
            session.rollback()

            log.error('Exception occurred while persisting DB objects: %s', e)
            raise


meta.mapper(HutemplateTagVocabulary, hutemplate_tag_table)
