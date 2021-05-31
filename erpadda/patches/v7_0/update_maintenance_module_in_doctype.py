# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.db.set_value("DocType", "Maintenance Schedule", "module", "Maintenance")
	vmraid.db.set_value("DocType", "Maintenance Schedule Detail", "module", "Maintenance")
	vmraid.db.set_value("DocType", "Maintenance Schedule Item", "module", "Maintenance")
	vmraid.db.set_value("DocType", "Maintenance Visit", "module", "Maintenance")
	vmraid.db.set_value("DocType", "Maintenance Visit Purpose", "module", "Maintenance")