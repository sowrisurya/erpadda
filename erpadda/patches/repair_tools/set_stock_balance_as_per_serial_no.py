# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	from erpadda.stock.stock_balance import set_stock_balance_as_per_serial_no
	vmraid.db.auto_commit_on_many_writes = 1

	set_stock_balance_as_per_serial_no()

	vmraid.db.auto_commit_on_many_writes = 0
