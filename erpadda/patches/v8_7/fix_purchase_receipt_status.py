from __future__ import unicode_literals
import vmraid

def execute():
	# there is no more status called "Submitted", there was an old issue that used
	# to set it as Submitted, fixed in this commit
	vmraid.db.sql("""
	update
		`tabPurchase Receipt`
	set
		status = 'To Bill'
	where
		status = 'Submitted'""")