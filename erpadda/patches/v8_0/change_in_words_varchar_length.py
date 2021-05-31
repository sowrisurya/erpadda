# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	doctypes = vmraid.db.sql_list("""select parent from tabDocField where fieldname = 'in_words'""")
		
	for dt in doctypes:
		for fieldname in ("in_words", "base_in_words"):
			vmraid.db.sql("alter table `tab{0}` change column `{1}` `{2}` varchar(255)"
				.format(dt, fieldname, fieldname))
				
	vmraid.db.sql("""alter table `tabJournal Entry` 
		change column `total_amount_in_words` `total_amount_in_words` varchar(255)""")
