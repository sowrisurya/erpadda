# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid
from erpadda.setup.install import default_mail_footer

def execute():
	return
	mail_footer = vmraid.db.get_default('mail_footer') or ''
	mail_footer += default_mail_footer
	vmraid.db.set_value("Outgoing Email Settings", "Outgoing Email Settings", "footer", mail_footer)
