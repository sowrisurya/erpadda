# -*- coding: utf-8 -*-
# Copyright (c) 2017, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.model.document import Document

class SupplierScorecardStanding(Document):
	pass


@vmraid.whitelist()
def get_scoring_standing(standing_name):
	standing = vmraid.get_doc("Supplier Scorecard Standing", standing_name)

	return standing


@vmraid.whitelist()
def get_standings_list():
	standings = vmraid.db.sql("""
		SELECT
			scs.name
		FROM
			`tabSupplier Scorecard Standing` scs""",
			{}, as_dict=1)

	return standings