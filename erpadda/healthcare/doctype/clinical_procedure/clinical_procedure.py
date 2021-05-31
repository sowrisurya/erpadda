# -*- coding: utf-8 -*-
# Copyright (c) 2017, ESS LLP and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid import _
from vmraid.model.document import Document
from vmraid.utils import flt, nowdate, nowtime, cstr
from erpadda.healthcare.doctype.healthcare_settings.healthcare_settings import get_account
from erpadda.healthcare.doctype.lab_test.lab_test import create_sample_doc
from erpadda.stock.stock_ledger import get_previous_sle
from erpadda.stock.get_item_details import get_item_details
from vmraid.model.mapper import get_mapped_doc

class ClinicalProcedure(Document):
	def validate(self):
		self.set_status()
		self.set_title()
		if self.consume_stock:
			self.set_actual_qty()

		if self.items:
			self.invoice_separately_as_consumables = False
			for item in self.items:
				if item.invoice_separately_as_consumables:
					self.invoice_separately_as_consumables = True

	def before_insert(self):
		if self.consume_stock:
			self.set_actual_qty()

	def after_insert(self):
		if self.prescription:
			vmraid.db.set_value('Procedure Prescription', self.prescription, 'procedure_created', 1)
		if self.appointment:
			vmraid.db.set_value('Patient Appointment', self.appointment, 'status', 'Closed')
		template = vmraid.get_doc('Clinical Procedure Template', self.procedure_template)
		if template.sample:
			patient = vmraid.get_doc('Patient', self.patient)
			sample_collection = create_sample_doc(template, patient, None, self.company)
			vmraid.db.set_value('Clinical Procedure', self.name, 'sample', sample_collection.name)
		self.reload()

	def set_status(self):
		if self.docstatus == 0:
			self.status = 'Draft'
		elif self.docstatus == 1:
			if self.status not in ['In Progress', 'Completed']:
				self.status = 'Pending'
		elif self.docstatus == 2:
			self.status = 'Cancelled'

	def set_title(self):
		self.title = _('{0} - {1}').format(self.patient_name or self.patient, self.procedure_template)[:100]

	@vmraid.whitelist()
	def complete_procedure(self):
		if self.consume_stock and self.items:
			stock_entry = make_stock_entry(self)

		if self.items:
			consumable_total_amount = 0
			consumption_details = False
			customer = vmraid.db.get_value('Patient', self.patient, 'customer')
			if customer:
				for item in self.items:
					if item.invoice_separately_as_consumables:
						price_list, price_list_currency = vmraid.db.get_values('Price List', {'selling': 1}, ['name', 'currency'])[0]
						args = {
							'doctype': 'Sales Invoice',
							'item_code': item.item_code,
							'company': self.company,
							'warehouse': self.warehouse,
							'customer': customer,
							'selling_price_list': price_list,
							'price_list_currency': price_list_currency,
							'plc_conversion_rate': 1.0,
							'conversion_rate': 1.0
						}
						item_details = get_item_details(args)
						item_price = item_details.price_list_rate * item.qty
						item_consumption_details = item_details.item_name + ' ' + str(item.qty) + ' ' + item.uom + ' ' + str(item_price)
						consumable_total_amount += item_price
						if not consumption_details:
							consumption_details = _('Clinical Procedure ({0}):').format(self.name)
						consumption_details += '\n\t' + item_consumption_details

				if consumable_total_amount > 0:
					vmraid.db.set_value('Clinical Procedure', self.name, 'consumable_total_amount', consumable_total_amount)
					vmraid.db.set_value('Clinical Procedure', self.name, 'consumption_details', consumption_details)
			else:
				vmraid.throw(_('Please set Customer in Patient {0}').format(vmraid.bold(self.patient)), title=_('Customer Not Found'))

		self.db_set('status', 'Completed')

		if self.consume_stock and self.items:
			return stock_entry

	@vmraid.whitelist()
	def start_procedure(self):
		allow_start = self.set_actual_qty()
		if allow_start:
			self.db_set('status', 'In Progress')
			return 'success'
		return 'insufficient stock'

	def set_actual_qty(self):
		allow_negative_stock = vmraid.db.get_single_value('Stock Settings', 'allow_negative_stock')

		allow_start = True
		for d in self.get('items'):
			d.actual_qty = get_stock_qty(d.item_code, self.warehouse)
			# validate qty
			if not allow_negative_stock and d.actual_qty < d.qty:
				allow_start = False
				break

		return allow_start

	@vmraid.whitelist()
	def make_material_receipt(self, submit=False):
		stock_entry = vmraid.new_doc('Stock Entry')

		stock_entry.stock_entry_type = 'Material Receipt'
		stock_entry.to_warehouse = self.warehouse
		stock_entry.company = self.company
		expense_account = get_account(None, 'expense_account', 'Healthcare Settings', self.company)
		for item in self.items:
			if item.qty > item.actual_qty:
				se_child = stock_entry.append('items')
				se_child.item_code = item.item_code
				se_child.item_name = item.item_name
				se_child.uom = item.uom
				se_child.stock_uom = item.stock_uom
				se_child.qty = flt(item.qty - item.actual_qty)
				se_child.t_warehouse = self.warehouse
				# in stock uom
				se_child.transfer_qty = flt(item.transfer_qty)
				se_child.conversion_factor = flt(item.conversion_factor)
				cost_center = vmraid.get_cached_value('Company',  self.company,  'cost_center')
				se_child.cost_center = cost_center
				se_child.expense_account = expense_account
		if submit:
			stock_entry.submit()
			return stock_entry
		return stock_entry.as_dict()


def get_stock_qty(item_code, warehouse):
	return get_previous_sle({
		'item_code': item_code,
		'warehouse': warehouse,
		'posting_date': nowdate(),
		'posting_time': nowtime()
	}).get('qty_after_transaction') or 0


@vmraid.whitelist()
def get_procedure_consumables(procedure_template):
	return get_items('Clinical Procedure Item', procedure_template, 'Clinical Procedure Template')


@vmraid.whitelist()
def set_stock_items(doc, stock_detail_parent, parenttype):
	items = get_items('Clinical Procedure Item', stock_detail_parent, parenttype)

	for item in items:
		se_child = doc.append('items')
		se_child.item_code = item.item_code
		se_child.item_name = item.item_name
		se_child.uom = item.uom
		se_child.stock_uom = item.stock_uom
		se_child.qty = flt(item.qty)
		# in stock uom
		se_child.transfer_qty = flt(item.transfer_qty)
		se_child.conversion_factor = flt(item.conversion_factor)
		if item.batch_no:
			se_child.batch_no = item.batch_no
		if parenttype == 'Clinical Procedure Template':
			se_child.invoice_separately_as_consumables = item.invoice_separately_as_consumables

	return doc


def get_items(table, parent, parenttype):
	items = vmraid.db.get_all(table, filters={
		'parent': parent,
		'parenttype': parenttype
	}, fields=['*'])

	return items


@vmraid.whitelist()
def make_stock_entry(doc):
	stock_entry = vmraid.new_doc('Stock Entry')
	stock_entry = set_stock_items(stock_entry, doc.name, 'Clinical Procedure')
	stock_entry.stock_entry_type = 'Material Issue'
	stock_entry.from_warehouse = doc.warehouse
	stock_entry.company = doc.company
	expense_account = get_account(None, 'expense_account', 'Healthcare Settings', doc.company)

	for item_line in stock_entry.items:
		cost_center = vmraid.get_cached_value('Company',  doc.company,  'cost_center')
		item_line.cost_center = cost_center
		item_line.expense_account = expense_account

	stock_entry.save(ignore_permissions=True)
	stock_entry.submit()
	return stock_entry.name


@vmraid.whitelist()
def make_procedure(source_name, target_doc=None):
	def set_missing_values(source, target):
		consume_stock = vmraid.db.get_value('Clinical Procedure Template', source.procedure_template, 'consume_stock')
		if consume_stock:
			target.consume_stock = 1
			warehouse = None
			if source.service_unit:
				warehouse = vmraid.db.get_value('Healthcare Service Unit', source.service_unit, 'warehouse')
			if not warehouse:
				warehouse = vmraid.db.get_value('Stock Settings', None, 'default_warehouse')
			if warehouse:
				target.warehouse = warehouse

			set_stock_items(target, source.procedure_template, 'Clinical Procedure Template')

	doc = get_mapped_doc('Patient Appointment', source_name, {
			'Patient Appointment': {
				'doctype': 'Clinical Procedure',
				'field_map': [
					['appointment', 'name'],
					['patient', 'patient'],
					['patient_age', 'patient_age'],
					['patient_sex', 'patient_sex'],
					['procedure_template', 'procedure_template'],
					['prescription', 'procedure_prescription'],
					['practitioner', 'practitioner'],
					['medical_department', 'department'],
					['start_date', 'appointment_date'],
					['start_time', 'appointment_time'],
					['notes', 'notes'],
					['service_unit', 'service_unit'],
					['company', 'company'],
					['invoiced', 'invoiced']
				]
			}
		}, target_doc, set_missing_values)

	return doc
