# -*- coding: utf-8 -*-
# Copyright (c) 2018, VMRaid Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import unittest
import vmraid
from vmraid.test_runner import make_test_records
from erpadda.stock.doctype.item.test_item import make_item
from erpadda.manufacturing.doctype.operation.test_operation import make_operation
from erpadda.manufacturing.doctype.job_card.job_card import OperationSequenceError
from erpadda.manufacturing.doctype.workstation.test_workstation import make_workstation
from erpadda.manufacturing.doctype.work_order.test_work_order import make_wo_order_test_record

class TestRouting(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.item_code = "Test Routing Item - A"

	@classmethod
	def tearDownClass(cls):
		vmraid.db.sql('delete from tabBOM where item=%s', cls.item_code)

	def test_sequence_id(self):
		operations = [{"operation": "Test Operation A", "workstation": "Test Workstation A", "time_in_mins": 30},
			{"operation": "Test Operation B", "workstation": "Test Workstation A", "time_in_mins": 20}]

		make_test_records("UOM")

		setup_operations(operations)
		routing_doc = create_routing(routing_name="Testing Route", operations=operations)
		bom_doc = setup_bom(item_code=self.item_code, routing=routing_doc.name)
		wo_doc = make_wo_order_test_record(production_item = self.item_code, bom_no=bom_doc.name)

		for row in routing_doc.operations:
			self.assertEqual(row.sequence_id, row.idx)

		for data in vmraid.get_all("Job Card",
			filters={"work_order": wo_doc.name}, order_by="sequence_id desc"):
			job_card_doc = vmraid.get_doc("Job Card", data.name)
			job_card_doc.time_logs[0].completed_qty = 10
			if job_card_doc.sequence_id != 1:
				self.assertRaises(OperationSequenceError, job_card_doc.save)
			else:
				job_card_doc.save()
				self.assertEqual(job_card_doc.total_completed_qty, 10)

		wo_doc.cancel()
		wo_doc.delete()

def setup_operations(rows):
	for row in rows:
		make_workstation(row)
		make_operation(row)

def create_routing(**args):
	args = vmraid._dict(args)

	doc = vmraid.new_doc("Routing")
	doc.update(args)

	if not args.do_not_save:
		try:
			for operation in args.operations:
				doc.append("operations", operation)

			doc.insert()
		except vmraid.DuplicateEntryError:
			doc = vmraid.get_doc("Routing", args.routing_name)

	return doc

def setup_bom(**args):
	from erpadda.manufacturing.doctype.production_plan.test_production_plan import make_bom

	args = vmraid._dict(args)

	if not vmraid.db.exists('Item', args.item_code):
		make_item(args.item_code, {
			'is_stock_item': 1
		})

	if not args.raw_materials:
		if not vmraid.db.exists('Item', "Test Extra Item N-1"):
			make_item("Test Extra Item N-1", {
				'is_stock_item': 1,
			})

		args.raw_materials = ['Test Extra Item N-1']

	name = vmraid.db.get_value('BOM', {'item': args.item_code}, 'name')
	if not name:
		bom_doc = make_bom(item = args.item_code, raw_materials = args.get("raw_materials"),
			routing = args.routing, with_operations=1)
	else:
		bom_doc = vmraid.get_doc("BOM", name)

	return bom_doc
