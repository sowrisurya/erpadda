# -*- coding: utf-8 -*-
# Copyright (c) 2017, earthians and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid, json
from vmraid import _
from vmraid.model.document import Document
from vmraid.model.rename_doc import rename_doc

class ClinicalProcedureTemplate(Document):
	def validate(self):
		self.enable_disable_item()

	def after_insert(self):
		create_item_from_template(self)

	def on_update(self):
		if self.change_in_item:
			self.update_item_and_item_price()

	def enable_disable_item(self):
		if self.is_billable:
			if self.disabled:
				vmraid.db.set_value('Item', self.item, 'disabled', 1)
			else:
				vmraid.db.set_value('Item', self.item, 'disabled', 0)

	def update_item_and_item_price(self):
		if self.is_billable and self.item:
			item_doc = vmraid.get_doc('Item', {'item_code': self.item})
			item_doc.item_name = self.template
			item_doc.item_group = self.item_group
			item_doc.description = self.description
			item_doc.disabled = 0
			item_doc.save(ignore_permissions=True)

			if self.rate:
				item_price = vmraid.get_doc('Item Price', {'item_code': self.item})
				item_price.item_name = self.template
				item_price.price_list_rate = self.rate
				item_price.save()

		elif not self.is_billable and self.item:
			vmraid.db.set_value('Item', self.item, 'disabled', 1)

		self.db_set('change_in_item', 0)


@vmraid.whitelist()
def get_item_details(args=None):
	if not isinstance(args, dict):
		args = json.loads(args)

	item = vmraid.db.get_all('Item',
		filters={
			'disabled': 0,
			'name': args.get('item_code')
		},
		fields=['stock_uom', 'item_name']
	)

	if not item:
		vmraid.throw(_('Item {0} is not active').format(args.get('item_code')))

	item = item[0]
	ret = {
		'uom': item.stock_uom,
		'stock_uom': item.stock_uom,
		'item_name': item.item_name,
		'qty': 1,
		'transfer_qty': 0,
		'conversion_factor': 1
	}
	return ret

def create_item_from_template(doc):
	disabled = doc.disabled
	if doc.is_billable and not doc.disabled:
		disabled = 0

	uom = vmraid.db.exists('UOM', 'Unit') or vmraid.db.get_single_value('Stock Settings', 'stock_uom')
	item = vmraid.get_doc({
		'doctype': 'Item',
		'item_code': doc.template,
		'item_name':doc.template,
		'item_group': doc.item_group,
		'description':doc.description,
		'is_sales_item': 1,
		'is_service_item': 1,
		'is_purchase_item': 0,
		'is_stock_item': 0,
		'show_in_website': 0,
		'is_pro_applicable': 0,
		'disabled': disabled,
		'stock_uom': uom
	}).insert(ignore_permissions=True, ignore_mandatory=True)

	make_item_price(item.name, doc.rate)
	doc.db_set('item', item.name)

def make_item_price(item, item_price):
	price_list_name = vmraid.db.get_value('Price List', {'selling': 1})
	vmraid.get_doc({
		'doctype': 'Item Price',
		'price_list': price_list_name,
		'item_code': item,
		'price_list_rate': item_price
	}).insert(ignore_permissions=True, ignore_mandatory=True)

@vmraid.whitelist()
def change_item_code_from_template(item_code, doc):
	doc = vmraid._dict(json.loads(doc))

	if vmraid.db.exists('Item', {'item_code': item_code}):
		vmraid.throw(_('Item with Item Code {0} already exists').format(item_code))
	else:
		rename_doc('Item', doc.item_code, item_code, ignore_permissions=True)
		vmraid.db.set_value('Clinical Procedure Template', doc.name, 'item_code', item_code)
	return

