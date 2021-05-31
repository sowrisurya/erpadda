# -*- coding: utf-8 -*-
# Copyright (c) 2020, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.model.document import Document
from vmraid import _

class GratuityRule(Document):

	def validate(self):
		for current_slab in self.gratuity_rule_slabs:
			if (current_slab.from_year > current_slab.to_year) and current_slab.to_year != 0:
				vmraid(_("Row {0}: From (Year) can not be greater than To (Year)").format(current_slab.idx))

			if current_slab.to_year == 0 and current_slab.from_year == 0 and len(self.gratuity_rule_slabs) > 1:
				vmraid.throw(_("You can not define multiple slabs if you have a slab with no lower and upper limits."))

def get_gratuity_rule(name, slabs, **args):
	args = vmraid._dict(args)

	rule = vmraid.new_doc("Gratuity Rule")
	rule.name = name
	rule.calculate_gratuity_amount_based_on = args.calculate_gratuity_amount_based_on or "Current Slab"
	rule.work_experience_calculation_method = args.work_experience_calculation_method or "Take Exact Completed Years"
	rule.minimum_year_for_gratuity = 1


	for slab in slabs:
		slab = vmraid._dict(slab)
		rule.append("gratuity_rule_slabs", slab)
	return rule
