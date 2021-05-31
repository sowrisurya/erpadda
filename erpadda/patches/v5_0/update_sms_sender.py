# Copyright (c) 2013, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.db.set_value("SMS Settings", "SMS Settings", "sms_sender_name",
		vmraid.db.get_single_value("Global Defaults", "sms_sender_name"))
