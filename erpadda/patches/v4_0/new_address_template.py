from __future__ import print_function, unicode_literals
import vmraid

def execute():
	vmraid.reload_doc("utilities", "doctype", "address_template")
	if not vmraid.db.sql("select name from `tabAddress Template`"):
		try:
			d = vmraid.new_doc("Address Template")
			d.update({"country":vmraid.db.get_default("country") or
				vmraid.db.get_value("Global Defaults", "Global Defaults", "country")})
			d.insert()
		except:
			print(vmraid.get_traceback())

