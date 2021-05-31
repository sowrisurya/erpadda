# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import vmraid

def execute():
	# delete bin indexes
	unwanted_indexes = ["item_code", "warehouse"]

	for k in unwanted_indexes:
		try:
			vmraid.db.sql("drop index {0} on `tabBin`".format(k))
		except:
			pass