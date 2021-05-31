# Copyright (c) 2016, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.utils import cstr

def execute():
	vmraid.reload_doc("stock", "doctype", "manufacturer")
	vmraid.reload_doctype("Item")
	
	for d in vmraid.db.sql("""select distinct manufacturer from tabItem 
		where ifnull(manufacturer, '') != '' and disabled=0"""):
			manufacturer_name = cstr(d[0]).strip()
			if manufacturer_name and not vmraid.db.exists("Manufacturer", manufacturer_name):
				man = vmraid.new_doc("Manufacturer")
				man.short_name = manufacturer_name
				man.full_name = manufacturer_name
				man.save()
