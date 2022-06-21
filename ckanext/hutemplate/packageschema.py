import ckan.plugins.toolkit as toolkit

class HuTemplateField():
    def __init__(self, field, label, type):
        self.field = field
        self.label = label
        self.type = type

def getPackageSchema():
    return [
        # HuTemplateField('', 'Kapcsolat', 'text'), #dcat:contactPoint -> extra:contact_uri
        HuTemplateField('contact_name', 'Kapcsolat neve', 'text'), #vcard:fn -> extra:contact_name
        HuTemplateField('contact_email', 'Kapcsolat email', 'email'), #vcard:hasEmail -> extra:contact_email
        # HuTemplateField('', 'Közzétevő', 'text'), #dct:publisher -> extra:publisher_uri Ez az organization
        HuTemplateField('spatial_uri', 'Térbeli lefedettség', 'text'), #dct:spatial -> extra:spatial_uri
        HuTemplateField('temporal_start', 'Időbeli lefedettség kezdete', 'date'), #dct:temporal -> extra:temporal_start + extra:temporal_end
        HuTemplateField('temporal_end', 'Időbeli lefedettség vége', 'date'), #dct:temporal -> extra:temporal_start + extra:temporal_end
        HuTemplateField('theme', 'Téma', 'list'), #dcat:theme -> extra:theme
        HuTemplateField('access_rights', 'Hozzáférési jogok', 'text'), #dct:accessRights -> extra:access_rights
        HuTemplateField('conforms_to', 'Megfelelések', 'list'), #dct:conformsTo -> extra:conforms_to
        HuTemplateField('documentation', 'Dokumentáció', 'list'), #foaf:page -> extra:documentation
# HuTemplateField('frequency', 'Frissítés gyakorisága', 'text'), #dct:accrualPeriodicity -> extra:frequency
        HuTemplateField('has_version', 'Változatok', 'list'), #dct:hasVersion -> extra:has_version
        HuTemplateField('identifier', 'Azonosító', 'text'), #dct:identifier -> extra:identifier
        HuTemplateField('is_version_of', 'Eredeti változat', 'list'), #dct:isVersionOf -> extra:is_version_of
# HuTemplateField('language', 'Nyelvek', 'list'), #dct:language -> extra:language
        HuTemplateField('alternate_identifier', 'Egyéb azonosító', 'text'), #adms:identifier -> extra:alternate_identifier
        HuTemplateField('provenance', 'Eredet', 'text'), #dct:provenance -> extra:provenance
        HuTemplateField('source', 'Források', 'list'), #dct:source -> extra:source
        HuTemplateField('dcat_type', 'Típus', 'text'), #dct:type -> 	extra:dcat_type
        HuTemplateField('version_notes', 'Verziójegyzetek', 'text') #adms:versionNotes -> extra:version_notes
    ]




def updateHuSchema(schema):
    for huSchema in getPackageSchema():
        schema.update({
            huSchema.field: [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')]
        })

def showHuSchema(schema):
    for huSchema in getPackageSchema():
        schema.update({
            huSchema.field: [toolkit.get_converter('convert_from_extras'), 
                            toolkit.get_validator('ignore_missing')]
        })