from __future__ import unicode_literals
import vmraid

def execute():
	for doctype in ("Sales Order", "Purchase Order"):
		data = vmraid.db.sql("""select parent, modified_by, modified
			from `tab{doctype} Item` where docstatus=1 group by parent""".format(doctype=doctype), as_dict=True)
		for item in data:
			vmraid.db.sql("""update `tab{doctype}` set modified_by=%(modified_by)s, modified=%(modified)s
				where name=%(parent)s""".format(doctype=doctype), item)
