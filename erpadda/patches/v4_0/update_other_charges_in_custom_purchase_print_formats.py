# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid
import re

def execute():
	for name, html in vmraid.db.sql("""select name, html from `tabPrint Format`
		where standard = 'No' and html like '%%purchase\\_tax\\_details%%'"""):
			html = re.sub(r"\bpurchase_tax_details\b", "taxes", html)
			vmraid.db.set_value("Print Format", name, "html", html)
