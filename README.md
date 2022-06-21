# ckanext-hutemplate

CKAN extension for the Hungarian Open Data portal

## Requirements

The extension was developed on CKAN version 2.9 

Other required extension:
* [ckanext-pages](https://github.com/ckan/ckanext-pages)
  
	for the CMS contents in the template
  
* [ckanext-dcat](https://github.com/ckan/ckanext-dcat)
  
	for the DCAT profile
  
* [ckanext-scheming](https://github.com/ckan/ckanext-scheming)
  
	for the metadata field schema configuration


## Installation

First have working 2.9 CKAN. Installation instuctions can be found on the [official CKAN website](http://docs.ckan.org/en/2.9/maintaining/installing/index.html)

To install ckanext-hutemplate:

1. Install the required extensions with their dependencies.

2. Install the ckanext-hutemplate extension with pip:

	```
	##
	pip install -e git+https://github.com/NAVU-Kft/nationalopendataportal.git#egg=ckanext-hutemplate
	```

3. Install the requirements for the ckanext-hutemplate extension with pip:
	```
	pip install -r ckanext-hutemplate/requirements.txt
	```

4. Add `hutemplate` to the `ckan.plugins` setting in your CKAN config file (by default the config file is located at `/etc/ckan/default/ckan.ini`).

5. Restart CKAN. For example if you've deployed CKAN with Apache OR Nginx on Ubuntu:

     ```
     sudo service apache2 reload
	 	 
	 sudo service nginx restart
     ```

## Config settings

### Configure the [ckanext-pages](https://github.com/ckan/ckanext-pages) extension:

Add `pages` to the `ckan.plugins` setting in your CKAN config file (by default the config file is located at `/etc/ckan/default/ckan.ini`).

```
ckan --config=$CKAN_INI pages initdb
ckan config-tool $CKAN_INI "ckanext.pages.editor = ckeditor"
```

### Configure the [ckanext-scheming](https://github.com/ckan/ckanext-scheming) extension:

Add `scheming_datasets scheming_groups scheming_organizations` to the `ckan.plugins` setting in your CKAN config file (by default the config file is located at `/etc/ckan/default/ckan.ini`).

```
ckan config-tool $CKAN_INI "scheming.dataset_schemas = ckanext.hutemplate:hutemplate_schema.yaml"
ckan config-tool $CKAN_INI "scheming.group_schemas = ckanext.hutemplate:group_fields.json"
ckan config-tool $CKAN_INI "scheming.organization_schemas = ckanext.hutemplate:org_fields.json"
ckan config-tool $CKAN_INI "scheming.presets = ckanext.scheming:presets.json ckanext.hutemplate:hutemplate_presets.json"
ckan config-tool $CKAN_INI "scheming.dataset_fallback = false"
```

### Configure the [Multilingual Extension](https://docs.ckan.org/en/2.9/maintaining/multilingual.html) extension:

Add `multilingual_group multilingual_tag` to the `ckan.plugins` setting in your CKAN config file (by default the config file is located at `/etc/ckan/default/ckan.ini`).

### Configure the rdf profile for [ckanext-dcat](https://github.com/ckan/ckanext-dcat):

Add `dcat dcat_rdf_harvester dcat_json_harvester dcat_json_interface structured_data` to the `ckan.plugins` setting in your CKAN config file (by default the config file is located at `/etc/ckan/default/ckan.ini`).

```
ckan --config=$CKAN_INI harvester initdb
ckan config-tool $CKAN_INI "ckanext.dcat.rdf.profiles = euro_dcat_ap hu_dcat_ap"
ckan config-tool $CKAN_INI "ckanext.dcat.translate_keys = false"
```

### Configure the prefered languages:

```
ckan config-tool $CKAN_INI "ckan.locale_default = hu"
ckan config-tool $CKAN_INI "ckan.locale_order = hu en"
ckan config-tool $CKAN_INI "ckan.locales_offered = hu en"
```

### Configure the tracking:
```
ckan config-tool $CKAN_INI "ckan.tracking_enabled = true"
```

### Set up cron jobs, to update the tracking data: 

See the [CKAN docs](https://docs.ckan.org/en/2.9/maintaining/tracking.html) for more information
Example:
```
@hourly ckan -c /etc/ckan/default/ckan.ini tracking update  && ckan -c /etc/ckan/default/ckan.ini search-index rebuild -r
```

### Configure Solr for the temporal interval filter:

To ensure, that the temporal interval filter works, configure the solr `<fields>` part by adding the following lines:
```
<field name="extras_temporal_start" type="date" indexed="true" stored="true" multiValued="false"/>
<field name="extras_temporal_end" type="date" indexed="true" stored="true" multiValued="false"/>
```

### Other configurations:
```
ckan config-tool $CKAN_INI "ckanext.hutemplate.github_url = https://github.com/NAVU-Kft/nationalopendataportal"
ckan config-tool $CKAN_INI "ckan.gravatar_default = disabled"
```

### Initialize the hutemplate database tables:

```
ckan --config=$CKAN_INI hutemplate initdb
```

### Load the vocabularies:

```
ckan --config=$CKAN_INI hutemplate load-all
```

### Check the plugins variable:
It should look similar to this:
```
ckan.plugins = hutemplate envvars datapusher pages harvest ckan_harvester dcat dcat_rdf_harvester dcat_json_harvester dcat_json_interface structured_data scheming_datasets multilingual_group multilingual_tag scheming_groups scheming_organizations
```

## Translating the plugin:

1. To extract the translatable strings, run:

```
docker-compose -f docker-compose.dev.yml exec ckan-dev /bin/bash -c "cd src_extensions/ckanext-hutemplate/ ; python3 setup.py extract_messages ; cat ckanext/hutemplate/i18n/ckan.pot >> ckanext/hutemplate/i18n/ckanext-hutemplate.pot ; cat ckanext/hutemplate/i18n/schema.pot >> ckanext/hutemplate/i18n/ckanext-hutemplate.pot ; cat ckanext/hutemplate/i18n/exceptions.pot >> ckanext/hutemplate/i18n/ckanext-hutemplate.pot"
```

2. To generate the PO catalog for a language, use:

```
docker-compose -f docker-compose.dev.yml exec ckan-dev /bin/bash -c "cd src_extensions/ckanext-hutemplate/ ; python3 setup.py update_catalog -l hu"
```

3. Translate in the PO file

4. To compile the translation, use:

```
docker-compose -f docker-compose.dev.yml exec ckan-dev /bin/bash -c "cd src_extensions/ckanext-hutemplate/ ; python3 setup.py compile_catalog"
```

## Loading vocabularies in the docker environment:

```
docker-compose -f docker-compose.dev.yml exec ckan-dev /bin/bash -c "ckan --config=ckan.ini hutemplate load-all" 
```
## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
