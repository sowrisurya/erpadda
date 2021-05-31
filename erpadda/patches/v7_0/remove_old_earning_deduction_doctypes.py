# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	if vmraid.db.exists("DocType", "Salary Component"):
		for dt in ("Salary Structure Earning", "Salary Structure Deduction", "Salary Slip Earning", 
			"Salary Slip Deduction", "Earning Type", "Deduction Type"):
				vmraid.delete_doc("DocType", dt)
				
					
		for d in vmraid.db.sql("""select name from `tabCustom Field` 
			where dt in ('Salary Detail', 'Salary Component')"""):
				vmraid.get_doc("Custom Field", d[0]).save()