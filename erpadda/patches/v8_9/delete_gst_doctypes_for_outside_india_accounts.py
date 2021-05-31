from __future__ import unicode_literals
import vmraid

def execute():
	company = vmraid.get_all('Company', filters = {'country': 'India'})
	if not company:
		if vmraid.db.exists("DocType", "GST Settings"):
			vmraid.delete_doc("DocType", "GST Settings")
			vmraid.delete_doc("DocType", "GST HSN Code")
		
			for report_name in ('GST Sales Register', 'GST Purchase Register',
				'GST Itemised Sales Register', 'GST Itemised Purchase Register'):

				vmraid.delete_doc('Report', report_name)