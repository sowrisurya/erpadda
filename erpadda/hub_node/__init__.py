# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid

@vmraid.whitelist()
def enable_hub():
	hub_settings = vmraid.get_doc('Marketplace Settings')
	hub_settings.register()
	vmraid.db.commit()
	return hub_settings

@vmraid.whitelist()
def sync():
	hub_settings = vmraid.get_doc('Marketplace Settings')
	hub_settings.sync()
