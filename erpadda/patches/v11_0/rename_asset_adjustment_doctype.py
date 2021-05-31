# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid


def execute():
	if vmraid.db.table_exists("Asset Adjustment") and not vmraid.db.table_exists("Asset Value Adjustment"):
		vmraid.rename_doc('DocType', 'Asset Adjustment', 'Asset Value Adjustment', force=True)
		vmraid.reload_doc('assets', 'doctype', 'asset_value_adjustment')