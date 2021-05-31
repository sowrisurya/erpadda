# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc("regional", "doctype", "gst_settings")
	vmraid.reload_doc("accounts", "doctype", "gst_account")
	gst_settings = vmraid.get_doc("GST Settings")
	gst_settings.b2c_limit = 250000
	gst_settings.save()
