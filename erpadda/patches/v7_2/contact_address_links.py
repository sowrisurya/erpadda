from __future__ import unicode_literals
import vmraid
from vmraid.core.doctype.dynamic_link.dynamic_link import deduplicate_dynamic_links
from vmraid.utils import update_progress_bar

def execute():
	vmraid.reload_doc('core', 'doctype', 'dynamic_link')
	vmraid.reload_doc('contacts', 'doctype', 'contact')
	vmraid.reload_doc('contacts', 'doctype', 'address')
	map_fields = (
		('Customer', 'customer'),
		('Supplier', 'supplier'),
		('Lead', 'lead'),
		('Sales Partner', 'sales_partner')
	)
	for doctype in ('Contact', 'Address'):
		if vmraid.db.has_column(doctype, 'customer'):
			items = vmraid.get_all(doctype)
			for i, doc in enumerate(items):
				doc = vmraid.get_doc(doctype, doc.name)
				dirty = False
				for field in map_fields:
					if doc.get(field[1]):
						doc.append('links', dict(link_doctype=field[0], link_name=doc.get(field[1])))
						dirty = True

					if dirty:
						deduplicate_dynamic_links(doc)
						doc.update_children()

					update_progress_bar('Updating {0}'.format(doctype), i, len(items))
			print