from __future__ import unicode_literals

import vmraid

def execute():
	vmraid.db.sql("""Update `tabItem` as item set default_bom = NULL where 
		not exists(select name from `tabBOM` as bom where item.default_bom = bom.name and bom.docstatus =1 )""")