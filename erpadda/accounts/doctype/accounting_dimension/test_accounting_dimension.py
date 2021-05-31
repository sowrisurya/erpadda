# -*- coding: utf-8 -*-
# Copyright (c) 2019, VMRaid Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import vmraid
import unittest
from erpadda.accounts.doctype.sales_invoice.test_sales_invoice import create_sales_invoice
from erpadda.accounts.doctype.journal_entry.test_journal_entry import make_journal_entry

test_dependencies = ['Cost Center', 'Location', 'Warehouse', 'Department']

class TestAccountingDimension(unittest.TestCase):
	def setUp(self):
		create_dimension()

	def test_dimension_against_sales_invoice(self):
		si = create_sales_invoice(do_not_save=1)

		si.location = "Block 1"
		si.append("items", {
			"item_code": "_Test Item",
			"warehouse": "_Test Warehouse - _TC",
			"qty": 1,
			"rate": 100,
			"income_account": "Sales - _TC",
			"expense_account": "Cost of Goods Sold - _TC",
			"cost_center": "_Test Cost Center - _TC",
			"department": "_Test Department - _TC",
			"location": "Block 1"
		})

		si.save()
		si.submit()

		gle = vmraid.get_doc("GL Entry", {"voucher_no": si.name, "account": "Sales - _TC"})

		self.assertEqual(gle.get('department'), "_Test Department - _TC")

	def test_dimension_against_journal_entry(self):
		je = make_journal_entry("Sales - _TC", "Sales Expenses - _TC", 500, save=False)
		je.accounts[0].update({"department": "_Test Department - _TC"})
		je.accounts[1].update({"department": "_Test Department - _TC"})

		je.accounts[0].update({"location": "Block 1"})
		je.accounts[1].update({"location": "Block 1"})

		je.save()
		je.submit()

		gle = vmraid.get_doc("GL Entry", {"voucher_no": je.name, "account": "Sales - _TC"})
		gle1 = vmraid.get_doc("GL Entry", {"voucher_no": je.name, "account": "Sales Expenses - _TC"})
		self.assertEqual(gle.get('department'), "_Test Department - _TC")
		self.assertEqual(gle1.get('department'), "_Test Department - _TC")

	def test_mandatory(self):
		si = create_sales_invoice(do_not_save=1)
		si.append("items", {
			"item_code": "_Test Item",
			"warehouse": "_Test Warehouse - _TC",
			"qty": 1,
			"rate": 100,
			"income_account": "Sales - _TC",
			"expense_account": "Cost of Goods Sold - _TC",
			"cost_center": "_Test Cost Center - _TC",
			"location": ""
		})

		si.save()
		self.assertRaises(vmraid.ValidationError, si.submit)

	def tearDown(self):
		disable_dimension()

def create_dimension():
	vmraid.set_user("Administrator")

	if not vmraid.db.exists("Accounting Dimension", {"document_type": "Department"}):
		vmraid.get_doc({
			"doctype": "Accounting Dimension",
			"document_type": "Department",
		}).insert()
	else:
		dimension = vmraid.get_doc("Accounting Dimension", "Department")
		dimension.disabled = 0
		dimension.save()

	if not vmraid.db.exists("Accounting Dimension", {"document_type": "Location"}):
		dimension1 = vmraid.get_doc({
			"doctype": "Accounting Dimension",
			"document_type": "Location",
		})

		dimension1.append("dimension_defaults", {
			"company": "_Test Company",
			"reference_document": "Location",
			"default_dimension": "Block 1",
			"mandatory_for_bs": 1
		})

		dimension1.insert()
		dimension1.save()
	else:
		dimension1 = vmraid.get_doc("Accounting Dimension", "Location")
		dimension1.disabled = 0
		dimension1.save()

def disable_dimension():
	dimension1 = vmraid.get_doc("Accounting Dimension", "Department")
	dimension1.disabled = 1
	dimension1.save()

	dimension2 = vmraid.get_doc("Accounting Dimension", "Location")
	dimension2.disabled = 1
	dimension2.save()

