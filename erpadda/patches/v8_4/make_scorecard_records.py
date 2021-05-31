# Copyright (c) 2017, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

from erpadda.buying.doctype.supplier_scorecard.supplier_scorecard import make_default_records
def execute():
	vmraid.reload_doc('buying', 'doctype', 'supplier_scorecard_variable')
	vmraid.reload_doc('buying', 'doctype', 'supplier_scorecard_standing')
	make_default_records()