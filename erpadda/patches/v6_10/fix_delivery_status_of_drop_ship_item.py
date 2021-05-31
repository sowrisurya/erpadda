from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype("Sales Order Item")
	for so_name in vmraid.db.sql("""select distinct parent from `tabSales Order Item`
			where delivered_by_supplier=1 and docstatus=1"""):
		so = vmraid.get_doc("Sales Order", so_name[0])
		so.update_delivery_status()
		so.set_status(update=True, update_modified=False)