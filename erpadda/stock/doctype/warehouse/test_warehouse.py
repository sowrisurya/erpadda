# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
from __future__ import unicode_literals

import unittest

import vmraid
from vmraid.utils import cint
from vmraid.test_runner import make_test_records

import erpadda
from erpadda.stock.doctype.stock_entry.stock_entry_utils import make_stock_entry
from erpadda.accounts.doctype.account.test_account import get_inventory_account, create_account

test_records = vmraid.get_test_records('Warehouse')

class TestWarehouse(unittest.TestCase):
	def setUp(self):
		if not vmraid.get_value('Item', '_Test Item'):
			make_test_records('Item')

	def test_parent_warehouse(self):
		parent_warehouse = vmraid.get_doc("Warehouse", "_Test Warehouse Group - _TC")
		self.assertEqual(parent_warehouse.is_group, 1)

	def test_warehouse_hierarchy(self):
		p_warehouse = vmraid.get_doc("Warehouse", "_Test Warehouse Group - _TC")

		child_warehouses =  vmraid.db.sql("""select name, is_group, parent_warehouse from `tabWarehouse` wh
			where wh.lft > %s and wh.rgt < %s""", (p_warehouse.lft, p_warehouse.rgt), as_dict=1)

		for child_warehouse in child_warehouses:
			self.assertEqual(p_warehouse.name, child_warehouse.parent_warehouse)
			self.assertEqual(child_warehouse.is_group, 0)

	def test_warehouse_renaming(self):
		create_warehouse("Test Warehouse for Renaming 1", company="_Test Company with perpetual inventory")
		account = get_inventory_account("_Test Company with perpetual inventory", "Test Warehouse for Renaming 1 - TCP1")
		self.assertTrue(vmraid.db.get_value("Warehouse", filters={"account": account}))

		# Rename with abbr
		if vmraid.db.exists("Warehouse", "Test Warehouse for Renaming 2 - TCP1"):
			vmraid.delete_doc("Warehouse", "Test Warehouse for Renaming 2 - TCP1")
		vmraid.rename_doc("Warehouse", "Test Warehouse for Renaming 1 - TCP1", "Test Warehouse for Renaming 2 - TCP1")

		self.assertTrue(vmraid.db.get_value("Warehouse",
			filters={"account": "Test Warehouse for Renaming 1 - TCP1"}))

		# Rename without abbr
		if vmraid.db.exists("Warehouse", "Test Warehouse for Renaming 3 - TCP1"):
			vmraid.delete_doc("Warehouse", "Test Warehouse for Renaming 3 - TCP1")

		vmraid.rename_doc("Warehouse", "Test Warehouse for Renaming 2 - TCP1", "Test Warehouse for Renaming 3")

		self.assertTrue(vmraid.db.get_value("Warehouse",
			filters={"account": "Test Warehouse for Renaming 1 - TCP1"}))

		# Another rename with multiple dashes
		if vmraid.db.exists("Warehouse", "Test - Warehouse - Company - TCP1"):
			vmraid.delete_doc("Warehouse", "Test - Warehouse - Company - TCP1")
		vmraid.rename_doc("Warehouse", "Test Warehouse for Renaming 3 - TCP1", "Test - Warehouse - Company")

	def test_warehouse_merging(self):
		company = "_Test Company with perpetual inventory"
		create_warehouse("Test Warehouse for Merging 1", company=company,
			properties={"parent_warehouse": "All Warehouses - TCP1"})
		create_warehouse("Test Warehouse for Merging 2", company=company,
			properties={"parent_warehouse": "All Warehouses - TCP1"})

		make_stock_entry(item_code="_Test Item", target="Test Warehouse for Merging 1 - TCP1",
			qty=1, rate=100, company=company)
		make_stock_entry(item_code="_Test Item", target="Test Warehouse for Merging 2 - TCP1",
			qty=1, rate=100, company=company)

		existing_bin_qty = (
			cint(vmraid.db.get_value("Bin",
				{"item_code": "_Test Item", "warehouse": "Test Warehouse for Merging 1 - TCP1"}, "actual_qty"))
			+ cint(vmraid.db.get_value("Bin",
				{"item_code": "_Test Item", "warehouse": "Test Warehouse for Merging 2 - TCP1"}, "actual_qty"))
		)

		vmraid.rename_doc("Warehouse", "Test Warehouse for Merging 1 - TCP1",
			"Test Warehouse for Merging 2 - TCP1", merge=True)

		self.assertFalse(vmraid.db.exists("Warehouse", "Test Warehouse for Merging 1 - TCP1"))

		bin_qty = vmraid.db.get_value("Bin",
			{"item_code": "_Test Item", "warehouse": "Test Warehouse for Merging 2 - TCP1"}, "actual_qty")

		self.assertEqual(bin_qty, existing_bin_qty)

		self.assertTrue(vmraid.db.get_value("Warehouse",
			filters={"account": "Test Warehouse for Merging 2 - TCP1"}))

def create_warehouse(warehouse_name, properties=None, company=None):
	if not company:
		company = "_Test Company"

	warehouse_id = erpadda.encode_company_abbr(warehouse_name, company)
	if not vmraid.db.exists("Warehouse", warehouse_id):
		w = vmraid.new_doc("Warehouse")
		w.warehouse_name = warehouse_name
		w.parent_warehouse = "_Test Warehouse Group - _TC"
		w.company = company
		w.account = get_warehouse_account(warehouse_name, company)
		if properties:
			w.update(properties)
		w.save()
		return w.name
	else:
		return warehouse_id

def get_warehouse(**args):
	args = vmraid._dict(args)
	if(vmraid.db.exists("Warehouse", args.warehouse_name + " - " + args.abbr)):
		return vmraid.get_doc("Warehouse", args.warehouse_name + " - " + args.abbr)
	else:
		w = vmraid.get_doc({
		"company": args.company or "_Test Company",
		"doctype": "Warehouse",
		"warehouse_name": args.warehouse_name,
		"is_group": 0,
		"account": get_warehouse_account(args.warehouse_name, args.company, args.abbr)
		})
		w.insert()
		return w

def get_warehouse_account(warehouse_name, company, company_abbr=None):
	if not company_abbr:
		company_abbr = vmraid.get_cached_value("Company", company, 'abbr')

	if not vmraid.db.exists("Account", warehouse_name + " - " + company_abbr):
		return create_account(
			account_name=warehouse_name,
			parent_account=get_group_stock_account(company, company_abbr),
			account_type='Stock',
			company=company)
	else:
		return warehouse_name + " - " + company_abbr


def get_group_stock_account(company, company_abbr=None):
	group_stock_account = vmraid.db.get_value("Account",
		filters={'account_type': 'Stock', 'is_group': 1, 'company': company}, fieldname='name')
	if not group_stock_account:
		if not company_abbr:
			company_abbr = vmraid.get_cached_value("Company", company, 'abbr')
		group_stock_account = "Current Assets - " + company_abbr
	return group_stock_account