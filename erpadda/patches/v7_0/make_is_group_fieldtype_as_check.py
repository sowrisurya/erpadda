from __future__ import unicode_literals
import vmraid

def execute():
	for doctype in ["Sales Person", "Customer Group", "Item Group", "Territory"]:
		
		# convert to 1 or 0
		vmraid.db.sql("update `tab{doctype}` set is_group = if(is_group='Yes',1,0) "
			.format(doctype=doctype))

		vmraid.db.commit()

		# alter fields to int
				
		vmraid.db.sql("alter table `tab{doctype}` change is_group is_group int(1) default '0'"
			.format(doctype=doctype))

		vmraid.reload_doctype(doctype)
