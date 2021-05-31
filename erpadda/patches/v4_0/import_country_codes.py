# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.geo.country_info import get_all
from vmraid.utils.install import import_country_and_currency

from six import iteritems

def execute():
	vmraid.reload_doc("setup", "doctype", "country")
	import_country_and_currency()
	for name, country in iteritems(get_all()):
		vmraid.set_value("Country", name, "code", country.get("code"))