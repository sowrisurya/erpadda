from __future__ import unicode_literals
import vmraid
from vmraid import _

def execute():
	from erpadda.setup.setup_wizard.operations.install_fixtures import default_lead_sources

	vmraid.reload_doc('crm', 'doctype', 'lead_source')

	vmraid.local.lang = vmraid.db.get_default("lang") or 'en'

	for s in default_lead_sources:
		insert_lead_source(_(s))

	# get lead sources in existing forms (customized)
	# and create a document if not created
	for d in ['Lead', 'Opportunity', 'Quotation', 'Sales Order', 'Delivery Note', 'Sales Invoice']:
		sources = vmraid.db.sql_list('select distinct source from `tab{0}`'.format(d))
		for s in sources:
			if s and s not in default_lead_sources:
				insert_lead_source(s)

		# remove customization for source
		for p in vmraid.get_all('Property Setter', {'doc_type':d, 'field_name':'source', 'property':'options'}):
			vmraid.delete_doc('Property Setter', p.name)

def insert_lead_source(s):
	if not vmraid.db.exists('Lead Source', s):
		vmraid.get_doc(dict(doctype='Lead Source', source_name=s)).insert()
