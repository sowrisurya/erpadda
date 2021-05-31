# -*- coding: utf-8 -*-
# Copyright (c) 2019, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.utils import get_datetime
from vmraid import _
from vmraid.model.document import Document
from erpadda.loan_management.doctype.loan_security_shortfall.loan_security_shortfall import check_for_ltv_shortfall

class ProcessLoanSecurityShortfall(Document):
	def onload(self):
		self.set_onload('update_time', get_datetime())

	def on_submit(self):
		check_for_ltv_shortfall(self.name)

def create_process_loan_security_shortfall():
	if check_for_secured_loans():
		process = vmraid.new_doc("Process Loan Security Shortfall")
		process.update_time = get_datetime()
		process.submit()

def check_for_secured_loans():
	return vmraid.db.count('Loan', {'docstatus': 1, 'is_secured_loan': 1})
