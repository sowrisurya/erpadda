from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.db.sql(
		"""UPDATE `tabPOS Profile` profile
		SET profile.`print_format` = 'POS Invoice'
		WHERE profile.`print_format` = 'Point of Sale'""")