# -*- coding: utf-8 -*-
# Copyright (c) 2019, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid import _
from vmraid.model.document import Document
from vmraid.utils import getdate, now_datetime, add_to_date, get_datetime, get_timestamp, get_datetime_str
from six import iteritems

class LoanSecurityPrice(Document):
	def validate(self):
		self.validate_dates()

	def validate_dates(self):

		if self.valid_from > self.valid_upto:
			vmraid.throw(_("Valid From Time must be lesser than Valid Upto Time."))

		existing_loan_security = vmraid.db.sql(""" SELECT name from `tabLoan Security Price`
			WHERE loan_security = %s AND name != %s AND (valid_from BETWEEN %s and %s OR valid_upto BETWEEN %s and %s) """,
			(self.loan_security, self.name, self.valid_from, self.valid_upto, self.valid_from, self.valid_upto))

		if existing_loan_security:
			vmraid.throw(_("Loan Security Price overlapping with {0}").format(existing_loan_security[0][0]))

@vmraid.whitelist()
def get_loan_security_price(loan_security, valid_time=None):
	if not valid_time:
		valid_time = get_datetime()

	loan_security_price = vmraid.db.get_value("Loan Security Price", {
		'loan_security': loan_security,
		'valid_from': ("<=",valid_time),
		'valid_upto': (">=", valid_time)
	}, 'loan_security_price')

	if not loan_security_price:
		vmraid.throw(_("No valid Loan Security Price found for {0}").format(vmraid.bold(loan_security)))
	else:
		return loan_security_price









