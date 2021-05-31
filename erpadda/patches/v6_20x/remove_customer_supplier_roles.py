from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc("buying", "doctype", "request_for_quotation_supplier")
	vmraid.reload_doc("buying", "doctype", "request_for_quotation_item")
	vmraid.reload_doc("buying", "doctype", "request_for_quotation")
	vmraid.reload_doc("projects", "doctype", "timesheet")
	
	for role in ('Customer', 'Supplier'):
		vmraid.db.sql('''delete from `tabHas Role`
			where role=%s and parent in ("Administrator", "Guest")''', role)

		if not vmraid.db.sql('select name from `tabHas Role` where role=%s', role):

			# delete DocPerm
			for doctype in vmraid.db.sql('select parent from tabDocPerm where role=%s', role):
				d = vmraid.get_doc("DocType", doctype[0])
				d.permissions = [p for p in d.permissions if p.role != role]
				d.save()

			# delete Role
			vmraid.delete_doc_if_exists('Role', role)
