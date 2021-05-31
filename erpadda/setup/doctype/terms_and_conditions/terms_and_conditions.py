# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid
from vmraid import _, throw
import json
from vmraid.model.document import Document
from vmraid.utils.jinja import validate_template
from vmraid.utils import cint

from six import string_types

class TermsandConditions(Document):
	def validate(self):
		if self.terms:
			validate_template(self.terms)
		if not cint(self.buying) and not cint(self.selling) and not cint(self.hr) and not cint(self.disabled):
			throw(_("At least one of the Applicable Modules should be selected"))

@vmraid.whitelist()
def get_terms_and_conditions(template_name, doc):
	if isinstance(doc, string_types):
		doc = json.loads(doc)

	terms_and_conditions = vmraid.get_doc("Terms and Conditions", template_name)
	
	if terms_and_conditions.terms:
		return vmraid.render_template(terms_and_conditions.terms, doc)