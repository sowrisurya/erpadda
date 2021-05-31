from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.db.sql("""UPDATE `tabDynamic Link` SET link_doctype = 'Lead' WHERE link_doctype = 'Load'""")
