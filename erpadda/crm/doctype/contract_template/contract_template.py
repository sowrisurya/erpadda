# -*- coding: utf-8 -*-
# Copyright (c) 2018, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.model.document import Document
from vmraid.utils.jinja import validate_template
from six import string_types
import json

class ContractTemplate(Document):
	def validate(self):
		if self.contract_terms:
			validate_template(self.contract_terms)

@vmraid.whitelist()
def get_contract_template(template_name, doc):
	if isinstance(doc, string_types):
		doc = json.loads(doc)

	contract_template = vmraid.get_doc("Contract Template", template_name)
	contract_terms = None

	if contract_template.contract_terms:
		contract_terms = vmraid.render_template(contract_template.contract_terms, doc)
	
	return {
		'contract_template': contract_template, 
		'contract_terms': contract_terms
	}