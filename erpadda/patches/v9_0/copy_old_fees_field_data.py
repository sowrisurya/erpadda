# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	# 'Schools' module changed to the 'Education'
	# vmraid.reload_doc("schools", "doctype", "fees")
	vmraid.reload_doc("education", "doctype", "fees")

	if "total_amount" not in vmraid.db.get_table_columns("Fees"):
		return

	vmraid.db.sql("""update tabFees set grand_total=total_amount where grand_total = 0.0""")