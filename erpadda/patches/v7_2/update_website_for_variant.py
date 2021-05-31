from __future__ import unicode_literals
import vmraid

def execute():
	# variant must have show_in_website = 0
	vmraid.reload_doctype('Item')
	vmraid.db.sql('''
		update tabItem set
			show_variant_in_website = 1,
			show_in_website = 0
		where
			show_in_website=1
			and ifnull(variant_of, "")!=""''')