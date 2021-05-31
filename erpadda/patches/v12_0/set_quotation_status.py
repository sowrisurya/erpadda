from __future__ import unicode_literals
import vmraid

def execute():

	vmraid.db.sql(""" UPDATE `tabQuotation` set status = 'Open'
		where docstatus = 1 and status = 'Submitted' """)