# -*- coding: utf-8 -*-
# Copyright (c) 2020, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid, erpadda
from rq.timeouts import JobTimeoutException
from vmraid.model.document import Document
from vmraid.utils import cint, get_link_to_form, add_to_date, now, today, time_diff_in_hours
from erpadda.stock.stock_ledger import repost_future_sle
from erpadda.accounts.utils import update_gl_entries_after, check_if_stock_and_account_balance_synced
from vmraid.utils.user import get_users_with_role
from vmraid import _
class RepostItemValuation(Document):
	def validate(self):
		self.set_status()
		self.reset_field_values()
		self.set_company()

	def reset_field_values(self):
		if self.based_on == 'Transaction':
			self.item_code = None
			self.warehouse = None
		else:
			self.voucher_type = None
			self.voucher_no = None

	def set_company(self):
		if self.voucher_type and self.voucher_no:
			self.company = vmraid.get_cached_value(self.voucher_type, self.voucher_no, "company")
		elif self.warehouse:
			self.company = vmraid.get_cached_value("Warehouse", self.warehouse, "company")

	def set_status(self, status=None):
		if not status:
			status = 'Queued'
		self.db_set('status', status)

	def on_submit(self):
		vmraid.enqueue(repost, timeout=1800, queue='long',
			job_name='repost_sle', now=vmraid.flags.in_test, doc=self)

	@vmraid.whitelist()
	def restart_reposting(self):
		self.set_status('Queued')
		vmraid.enqueue(repost, timeout=1800, queue='long',
			job_name='repost_sle', now=True, doc=self)

def repost(doc):
	try:
		if not vmraid.db.exists("Repost Item Valuation", doc.name):
			return

		doc.set_status('In Progress')
		vmraid.db.commit()

		repost_sl_entries(doc)
		repost_gl_entries(doc)

		doc.set_status('Completed')

	except (Exception, JobTimeoutException):
		vmraid.db.rollback()
		traceback = vmraid.get_traceback()
		vmraid.log_error(traceback)

		message = vmraid.message_log.pop()
		if traceback:
			message += "<br>" + "Traceback: <br>" + traceback
		vmraid.db.set_value(doc.doctype, doc.name, 'error_log', message)

		notify_error_to_stock_managers(doc, message)
		doc.set_status('Failed')
		raise
	finally:
		vmraid.db.commit()

def repost_sl_entries(doc):
	if doc.based_on == 'Transaction':
		repost_future_sle(voucher_type=doc.voucher_type, voucher_no=doc.voucher_no,
			allow_negative_stock=doc.allow_negative_stock, via_landed_cost_voucher=doc.via_landed_cost_voucher)
	else:
		repost_future_sle(args=[vmraid._dict({
			"item_code": doc.item_code,
			"warehouse": doc.warehouse,
			"posting_date": doc.posting_date,
			"posting_time": doc.posting_time
		})], allow_negative_stock=doc.allow_negative_stock, via_landed_cost_voucher=doc.via_landed_cost_voucher)

def repost_gl_entries(doc):
	if not cint(erpadda.is_perpetual_inventory_enabled(doc.company)):
		return

	if doc.based_on == 'Transaction':
		ref_doc = vmraid.get_doc(doc.voucher_type, doc.voucher_no)
		items, warehouses = ref_doc.get_items_and_warehouses()
	else:
		items = [doc.item_code]
		warehouses = [doc.warehouse]

	update_gl_entries_after(doc.posting_date, doc.posting_time,
		warehouses, items, company=doc.company)

def notify_error_to_stock_managers(doc, traceback):
	recipients = get_users_with_role("Stock Manager")
	if not recipients:
		get_users_with_role("System Manager")

	subject = _("Error while reposting item valuation")
	message = (_("Hi,") + "<br>"
		+ _("An error has been appeared while reposting item valuation via {0}")
			.format(get_link_to_form(doc.doctype, doc.name)) + "<br>"
		+ _("Please check the error message and take necessary actions to fix the error and then restart the reposting again.")
	)
	vmraid.sendmail(recipients=recipients, subject=subject, message=message)

def repost_entries():
	job_log = vmraid.get_all('Scheduled Job Log', fields = ['status', 'creation'],
		filters = {'scheduled_job_type': 'repost_item_valuation.repost_entries'}, order_by='creation desc', limit=1)

	if job_log and job_log[0]['status'] == 'Start' and time_diff_in_hours(now(), job_log[0]['creation']) < 2:
		return

	riv_entries = get_repost_item_valuation_entries()

	for row in riv_entries:
		doc = vmraid.get_cached_doc('Repost Item Valuation', row.name)
		repost(doc)

	riv_entries = get_repost_item_valuation_entries()
	if riv_entries:
		return

	for d in vmraid.get_all('Company', filters= {'enable_perpetual_inventory': 1}):
		check_if_stock_and_account_balance_synced(today(), d.name)

def get_repost_item_valuation_entries():
	date = add_to_date(now(), hours=-3)

	return vmraid.db.sql(""" SELECT name from `tabRepost Item Valuation`
		WHERE status != 'Completed' and creation <= %s and docstatus = 1
		ORDER BY timestamp(posting_date, posting_time) asc, creation asc
	""", date, as_dict=1)