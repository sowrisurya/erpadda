# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid
from erpadda.setup.doctype.company.company import install_country_fixtures

def execute():
	vmraid.reload_doc("accounts", "doctype", "account")
	vmraid.reload_doc("accounts", "doctype", "payment_schedule")
	for d in vmraid.get_all('Company',
		filters={'country': ('in', ['Saudi Arabia', 'United Arab Emirates'])}):
		install_country_fixtures(d.name)