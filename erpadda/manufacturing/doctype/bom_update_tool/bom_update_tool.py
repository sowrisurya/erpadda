# -*- coding: utf-8 -*-
# Copyright (c) 2017, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid, json
from vmraid.utils import cstr, flt
from vmraid import _
from six import string_types
from erpadda.manufacturing.doctype.bom.bom import get_boms_in_bottom_up_order
from vmraid.model.document import Document
import click

class BOMUpdateTool(Document):
	def replace_bom(self):
		self.validate_bom()

		unit_cost = get_new_bom_unit_cost(self.new_bom)
		self.update_new_bom(unit_cost)

		vmraid.cache().delete_key('bom_children')
		bom_list = self.get_parent_boms(self.new_bom)

		with click.progressbar(bom_list) as bom_list:
			pass
		for bom in bom_list:
			try:
				bom_obj = vmraid.get_cached_doc('BOM', bom)
				# this is only used for versioning and we do not want
				# to make separate db calls by using load_doc_before_save
				# which proves to be expensive while doing bulk replace
				bom_obj._doc_before_save = bom_obj
				bom_obj.update_new_bom(self.current_bom, self.new_bom, unit_cost)
				bom_obj.update_exploded_items()
				bom_obj.calculate_cost()
				bom_obj.update_parent_cost()
				bom_obj.db_update()
				if bom_obj.meta.get('track_changes') and not bom_obj.flags.ignore_version:
					bom_obj.save_version()
			except Exception:
				vmraid.log_error(vmraid.get_traceback())

	def validate_bom(self):
		if cstr(self.current_bom) == cstr(self.new_bom):
			vmraid.throw(_("Current BOM and New BOM can not be same"))

		if vmraid.db.get_value("BOM", self.current_bom, "item") \
			!= vmraid.db.get_value("BOM", self.new_bom, "item"):
				vmraid.throw(_("The selected BOMs are not for the same item"))

	def update_new_bom(self, unit_cost):
		vmraid.db.sql("""update `tabBOM Item` set bom_no=%s,
			rate=%s, amount=stock_qty*%s where bom_no = %s and docstatus < 2 and parenttype='BOM'""",
			(self.new_bom, unit_cost, unit_cost, self.current_bom))

	def get_parent_boms(self, bom, bom_list=None):
		if bom_list is None:
			bom_list = []
		data = vmraid.db.sql("""SELECT DISTINCT parent FROM `tabBOM Item`
			WHERE bom_no = %s AND docstatus < 2 AND parenttype='BOM'""", bom)

		for d in data:
			if self.new_bom == d[0]:
				vmraid.throw(_("BOM recursion: {0} cannot be child of {1}").format(bom, self.new_bom))

			bom_list.append(d[0])
			self.get_parent_boms(d[0], bom_list)

		return list(set(bom_list))

def get_new_bom_unit_cost(bom):
	new_bom_unitcost = vmraid.db.sql("""SELECT `total_cost`/`quantity`
		FROM `tabBOM` WHERE name = %s""", bom)

	return flt(new_bom_unitcost[0][0]) if new_bom_unitcost else 0

@vmraid.whitelist()
def enqueue_replace_bom(args):
	if isinstance(args, string_types):
		args = json.loads(args)

	vmraid.enqueue("erpadda.manufacturing.doctype.bom_update_tool.bom_update_tool.replace_bom", args=args, timeout=40000)
	vmraid.msgprint(_("Queued for replacing the BOM. It may take a few minutes."))

@vmraid.whitelist()
def enqueue_update_cost():
	vmraid.enqueue("erpadda.manufacturing.doctype.bom_update_tool.bom_update_tool.update_cost", timeout=40000)
	vmraid.msgprint(_("Queued for updating latest price in all Bill of Materials. It may take a few minutes."))

def update_latest_price_in_all_boms():
	if vmraid.db.get_single_value("Manufacturing Settings", "update_bom_costs_automatically"):
		update_cost()

def replace_bom(args):
	vmraid.db.auto_commit_on_many_writes = 1
	args = vmraid._dict(args)

	doc = vmraid.get_doc("BOM Update Tool")
	doc.current_bom = args.current_bom
	doc.new_bom = args.new_bom
	doc.replace_bom()

	vmraid.db.auto_commit_on_many_writes = 0

def update_cost():
	vmraid.db.auto_commit_on_many_writes = 1
	bom_list = get_boms_in_bottom_up_order()
	for bom in bom_list:
		vmraid.get_doc("BOM", bom).update_cost(update_parent=False, from_child_bom=True)

	vmraid.db.auto_commit_on_many_writes = 0
