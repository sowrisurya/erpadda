# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import unittest
import vmraid
import json

from vmraid.test_runner import make_test_objects
from erpadda.controllers.item_variant import (create_variant, ItemVariantExistsError,
	InvalidItemAttributeValueError, get_variant)
from erpadda.stock.doctype.item.item import StockExistsForTemplate, InvalidBarcode
from erpadda.stock.doctype.item.item import get_uom_conv_factor
from erpadda.stock.doctype.stock_entry.stock_entry_utils import make_stock_entry
from erpadda.stock.get_item_details import get_item_details

from six import iteritems

test_ignore = ["BOM"]
test_dependencies = ["Warehouse", "Item Group", "Item Tax Template", "Brand"]

def make_item(item_code, properties=None):
	if vmraid.db.exists("Item", item_code):
		return vmraid.get_doc("Item", item_code)

	item = vmraid.get_doc({
		"doctype": "Item",
		"item_code": item_code,
		"item_name": item_code,
		"description": item_code,
		"item_group": "Products"
	})

	if properties:
		item.update(properties)

	if item.is_stock_item:
		for item_default in [doc for doc in item.get("item_defaults") if not doc.default_warehouse]:
			item_default.default_warehouse = "_Test Warehouse - _TC"
			item_default.company = "_Test Company"
	item.insert()

	return item

class TestItem(unittest.TestCase):
	def setUp(self):
		vmraid.flags.attribute_values = None

	def get_item(self, idx):
		item_code = test_records[idx].get("item_code")
		if not vmraid.db.exists("Item", item_code):
			item = vmraid.copy_doc(test_records[idx])
			item.insert()
		else:
			item = vmraid.get_doc("Item", item_code)
		return item

	def test_get_item_details(self):
		# delete modified item price record and make as per test_records
		vmraid.db.sql("""delete from `tabItem Price`""")

		to_check = {
			"item_code": "_Test Item",
			"item_name": "_Test Item",
			"description": "_Test Item 1",
			"warehouse": "_Test Warehouse - _TC",
			"income_account": "Sales - _TC",
			"expense_account": "_Test Account Cost for Goods Sold - _TC",
			"cost_center": "_Test Cost Center - _TC",
			"qty": 1.0,
			"price_list_rate": 100.0,
			"base_price_list_rate": 0.0,
			"discount_percentage": 0.0,
			"rate": 0.0,
			"base_rate": 0.0,
			"amount": 0.0,
			"base_amount": 0.0,
			"batch_no": None,
			"uom": "_Test UOM",
			"conversion_factor": 1.0,
		}

		make_test_objects("Item Price")

		details = get_item_details({
			"item_code": "_Test Item",
			"company": "_Test Company",
			"price_list": "_Test Price List",
			"currency": "_Test Currency",
			"doctype": "Sales Order",
			"conversion_rate": 1,
			"price_list_currency": "_Test Currency",
			"plc_conversion_rate": 1,
			"order_type": "Sales",
			"customer": "_Test Customer",
			"conversion_factor": 1,
			"price_list_uom_dependant": 1,
			"ignore_pricing_rule": 1
		})

		for key, value in iteritems(to_check):
			self.assertEqual(value, details.get(key))

	def test_item_tax_template(self):
		expected_item_tax_template = [
			{"item_code": "_Test Item With Item Tax Template", "tax_category": "",
				"item_tax_template": "_Test Account Excise Duty @ 10 - _TC"},
			{"item_code": "_Test Item With Item Tax Template", "tax_category": "_Test Tax Category 1",
				"item_tax_template": "_Test Account Excise Duty @ 12 - _TC"},
			{"item_code": "_Test Item With Item Tax Template", "tax_category": "_Test Tax Category 2",
				"item_tax_template": None},

			{"item_code": "_Test Item Inherit Group Item Tax Template 1", "tax_category": "",
				"item_tax_template": "_Test Account Excise Duty @ 10 - _TC"},
			{"item_code": "_Test Item Inherit Group Item Tax Template 1", "tax_category": "_Test Tax Category 1",
				"item_tax_template": "_Test Account Excise Duty @ 12 - _TC"},
			{"item_code": "_Test Item Inherit Group Item Tax Template 1", "tax_category": "_Test Tax Category 2",
				"item_tax_template": None},

			{"item_code": "_Test Item Inherit Group Item Tax Template 2", "tax_category": "",
				"item_tax_template": "_Test Account Excise Duty @ 15 - _TC"},
			{"item_code": "_Test Item Inherit Group Item Tax Template 2", "tax_category": "_Test Tax Category 1",
				"item_tax_template": "_Test Account Excise Duty @ 12 - _TC"},
			{"item_code": "_Test Item Inherit Group Item Tax Template 2", "tax_category": "_Test Tax Category 2",
				"item_tax_template": None},

			{"item_code": "_Test Item Override Group Item Tax Template", "tax_category": "",
				"item_tax_template": "_Test Account Excise Duty @ 20 - _TC"},
			{"item_code": "_Test Item Override Group Item Tax Template", "tax_category": "_Test Tax Category 1",
				"item_tax_template": "_Test Item Tax Template 1 - _TC"},
			{"item_code": "_Test Item Override Group Item Tax Template", "tax_category": "_Test Tax Category 2",
				"item_tax_template": None},
		]

		expected_item_tax_map = {
			None: {},
			"_Test Account Excise Duty @ 10 - _TC": {"_Test Account Excise Duty - _TC": 10},
			"_Test Account Excise Duty @ 12 - _TC": {"_Test Account Excise Duty - _TC": 12},
			"_Test Account Excise Duty @ 15 - _TC": {"_Test Account Excise Duty - _TC": 15},
			"_Test Account Excise Duty @ 20 - _TC": {"_Test Account Excise Duty - _TC": 20},
			"_Test Item Tax Template 1 - _TC": {"_Test Account Excise Duty - _TC": 5, "_Test Account Education Cess - _TC": 10,
				"_Test Account S&H Education Cess - _TC": 15}
		}

		for data in expected_item_tax_template:
			details = get_item_details({
				"item_code": data['item_code'],
				"tax_category": data['tax_category'],
				"company": "_Test Company",
				"price_list": "_Test Price List",
				"currency": "_Test Currency",
				"doctype": "Sales Order",
				"conversion_rate": 1,
				"price_list_currency": "_Test Currency",
				"plc_conversion_rate": 1,
				"order_type": "Sales",
				"customer": "_Test Customer",
				"conversion_factor": 1,
				"price_list_uom_dependant": 1,
				"ignore_pricing_rule": 1
			})

			self.assertEqual(details.item_tax_template, data['item_tax_template'])
			self.assertEqual(json.loads(details.item_tax_rate), expected_item_tax_map[details.item_tax_template])

	def test_item_defaults(self):
		vmraid.delete_doc_if_exists("Item", "Test Item With Defaults", force=1)
		make_item("Test Item With Defaults", {
			"item_group": "_Test Item Group",
			"brand": "_Test Brand With Item Defaults",
			"item_defaults": [{
				"company": "_Test Company",
				"default_warehouse": "_Test Warehouse 2 - _TC",  # no override
				"expense_account": "_Test Account Stock Expenses - _TC",  # override brand default
				"buying_cost_center": "_Test Write Off Cost Center - _TC",  # override item group default
			}]
		})

		sales_item_check = {
			"item_code": "Test Item With Defaults",
			"warehouse": "_Test Warehouse 2 - _TC",  # from item
			"income_account": "_Test Account Sales - _TC",  # from brand
			"expense_account": "_Test Account Stock Expenses - _TC",  # from item
			"cost_center": "_Test Cost Center 2 - _TC",  # from item group
		}
		sales_item_details = get_item_details({
			"item_code": "Test Item With Defaults",
			"company": "_Test Company",
			"price_list": "_Test Price List",
			"currency": "_Test Currency",
			"doctype": "Sales Invoice",
			"conversion_rate": 1,
			"price_list_currency": "_Test Currency",
			"plc_conversion_rate": 1,
			"customer": "_Test Customer",
		})
		for key, value in iteritems(sales_item_check):
			self.assertEqual(value, sales_item_details.get(key))

		purchase_item_check = {
			"item_code": "Test Item With Defaults",
			"warehouse": "_Test Warehouse 2 - _TC",  # from item
			"expense_account": "_Test Account Stock Expenses - _TC",  # from item
			"income_account": "_Test Account Sales - _TC",  # from brand
			"cost_center": "_Test Write Off Cost Center - _TC"  # from item
		}
		purchase_item_details = get_item_details({
			"item_code": "Test Item With Defaults",
			"company": "_Test Company",
			"price_list": "_Test Price List",
			"currency": "_Test Currency",
			"doctype": "Purchase Invoice",
			"conversion_rate": 1,
			"price_list_currency": "_Test Currency",
			"plc_conversion_rate": 1,
			"supplier": "_Test Supplier",
		})
		for key, value in iteritems(purchase_item_check):
			self.assertEqual(value, purchase_item_details.get(key))

	def test_item_attribute_change_after_variant(self):
		vmraid.delete_doc_if_exists("Item", "_Test Variant Item-L", force=1)

		variant = create_variant("_Test Variant Item", {"Test Size": "Large"})
		variant.save()

		attribute = vmraid.get_doc('Item Attribute', 'Test Size')
		attribute.item_attribute_values = []

		# reset flags
		vmraid.flags.attribute_values = None

		self.assertRaises(InvalidItemAttributeValueError, attribute.save)
		vmraid.db.rollback()

	def test_make_item_variant(self):
		vmraid.delete_doc_if_exists("Item", "_Test Variant Item-L", force=1)

		variant = create_variant("_Test Variant Item", {"Test Size": "Large"})
		variant.save()

		# doing it again should raise error
		variant = create_variant("_Test Variant Item", {"Test Size": "Large"})
		variant.item_code = "_Test Variant Item-L-duplicate"
		self.assertRaises(ItemVariantExistsError, variant.save)

	def test_copy_fields_from_template_to_variants(self):
		vmraid.delete_doc_if_exists("Item", "_Test Variant Item-XL", force=1)

		fields = [{'field_name': 'item_group'}, {'field_name': 'is_stock_item'}]
		allow_fields = [d.get('field_name') for d in fields]
		set_item_variant_settings(fields)

		if not vmraid.db.get_value('Item Attribute Value',
			{'parent': 'Test Size', 'attribute_value': 'Extra Large'}, 'name'):
			item_attribute = vmraid.get_doc('Item Attribute', 'Test Size')
			item_attribute.append('item_attribute_values', {
				'attribute_value' : 'Extra Large',
				'abbr': 'XL'
			})
			item_attribute.save()

		template = vmraid.get_doc('Item', '_Test Variant Item')
		template.item_group = "_Test Item Group D"
		template.save()

		variant = create_variant("_Test Variant Item", {"Test Size": "Extra Large"})
		variant.item_code = "_Test Variant Item-XL"
		variant.item_name = "_Test Variant Item-XL"
		variant.save()

		variant = vmraid.get_doc('Item', '_Test Variant Item-XL')
		for fieldname in allow_fields:
			self.assertEqual(template.get(fieldname), variant.get(fieldname))

		template = vmraid.get_doc('Item', '_Test Variant Item')
		template.item_group = "_Test Item Group Desktops"
		template.save()

	def test_make_item_variant_with_numeric_values(self):
		# cleanup
		for d in vmraid.db.get_all('Item', filters={'variant_of':
				'_Test Numeric Template Item'}):
			vmraid.delete_doc_if_exists("Item", d.name)

		vmraid.delete_doc_if_exists("Item", "_Test Numeric Template Item")
		vmraid.delete_doc_if_exists("Item Attribute", "Test Item Length")

		vmraid.db.sql('''delete from `tabItem Variant Attribute`
			where attribute="Test Item Length"''')

		vmraid.flags.attribute_values = None

		# make item attribute
		vmraid.get_doc({
			"doctype": "Item Attribute",
			"attribute_name": "Test Item Length",
			"numeric_values": 1,
			"from_range": 0.0,
			"to_range": 100.0,
			"increment": 0.5
		}).insert()

		# make template item
		make_item("_Test Numeric Template Item", {
			"attributes": [
				{
					"attribute": "Test Size"
				},
				{
					"attribute": "Test Item Length",
					"numeric_values": 1,
					"from_range": 0.0,
					"to_range": 100.0,
					"increment": 0.5
				}
			],
			"item_defaults": [
				{
					"default_warehouse": "_Test Warehouse - _TC",
					"company": "_Test Company"
				}
			],
			"has_variants": 1
		})

		variant = create_variant("_Test Numeric Template Item",
			{"Test Size": "Large", "Test Item Length": 1.1})
		self.assertEqual(variant.item_code, "_Test Numeric Template Item-L-1.1")
		variant.item_code = "_Test Numeric Variant-L-1.1"
		variant.item_name = "_Test Numeric Variant Large 1.1m"
		self.assertRaises(InvalidItemAttributeValueError, variant.save)

		variant = create_variant("_Test Numeric Template Item",
			{"Test Size": "Large", "Test Item Length": 1.5})
		self.assertEqual(variant.item_code, "_Test Numeric Template Item-L-1.5")
		variant.item_code = "_Test Numeric Variant-L-1.5"
		variant.item_name = "_Test Numeric Variant Large 1.5m"
		variant.save()

	def test_item_merging(self):
		create_item("Test Item for Merging 1")
		create_item("Test Item for Merging 2")

		make_stock_entry(item_code="Test Item for Merging 1", target="_Test Warehouse - _TC",
			qty=1, rate=100)
		make_stock_entry(item_code="Test Item for Merging 2", target="_Test Warehouse 1 - _TC",
			qty=1, rate=100)

		vmraid.rename_doc("Item", "Test Item for Merging 1", "Test Item for Merging 2", merge=True)

		self.assertFalse(vmraid.db.exists("Item", "Test Item for Merging 1"))

		self.assertTrue(vmraid.db.get_value("Bin",
			{"item_code": "Test Item for Merging 2", "warehouse": "_Test Warehouse - _TC"}))

		self.assertTrue(vmraid.db.get_value("Bin",
			{"item_code": "Test Item for Merging 2", "warehouse": "_Test Warehouse 1 - _TC"}))

	def test_uom_conversion_factor(self):
		if vmraid.db.exists('Item', 'Test Item UOM'):
			vmraid.delete_doc('Item', 'Test Item UOM')

		item_doc = make_item("Test Item UOM", {
			"stock_uom": "Gram",
			"uoms": [dict(uom='Carat'), dict(uom='Kg')]
		})

		for d in item_doc.uoms:
			value = get_uom_conv_factor(d.uom, item_doc.stock_uom)
			d.conversion_factor = value

		self.assertEqual(item_doc.uoms[0].uom, "Carat")
		self.assertEqual(item_doc.uoms[0].conversion_factor, 0.2)
		self.assertEqual(item_doc.uoms[1].uom, "Kg")
		self.assertEqual(item_doc.uoms[1].conversion_factor, 1000)

	def test_item_variant_by_manufacturer(self):
		fields = [{'field_name': 'description'}, {'field_name': 'variant_based_on'}]
		set_item_variant_settings(fields)

		if vmraid.db.exists('Item', '_Test Variant Mfg'):
			vmraid.delete_doc('Item', '_Test Variant Mfg')
		if vmraid.db.exists('Item', '_Test Variant Mfg-1'):
			vmraid.delete_doc('Item', '_Test Variant Mfg-1')
		if vmraid.db.exists('Manufacturer', 'MSG1'):
			vmraid.delete_doc('Manufacturer', 'MSG1')

		template = vmraid.get_doc(dict(
			doctype='Item',
			item_code='_Test Variant Mfg',
			has_variant=1,
			item_group='Products',
			variant_based_on='Manufacturer'
		)).insert()

		manufacturer = vmraid.get_doc(dict(
			doctype='Manufacturer',
			short_name='MSG1'
		)).insert()

		variant = get_variant(template.name, manufacturer=manufacturer.name)
		self.assertEqual(variant.item_code, '_Test Variant Mfg-1')
		self.assertEqual(variant.description, '_Test Variant Mfg')
		self.assertEqual(variant.manufacturer, 'MSG1')
		variant.insert()

		variant = get_variant(template.name, manufacturer=manufacturer.name,
			manufacturer_part_no='007')
		self.assertEqual(variant.item_code, '_Test Variant Mfg-2')
		self.assertEqual(variant.description, '_Test Variant Mfg')
		self.assertEqual(variant.manufacturer, 'MSG1')
		self.assertEqual(variant.manufacturer_part_no, '007')

	def test_stock_exists_against_template_item(self):
		stock_item = vmraid.get_all('Stock Ledger Entry', fields = ["item_code"], limit=1)
		if stock_item:
			item_code = stock_item[0].item_code

			item_doc = vmraid.get_doc('Item', item_code)
			item_doc.has_variants = 1
			self.assertRaises(StockExistsForTemplate, item_doc.save)

	def test_add_item_barcode(self):
		# Clean up
		vmraid.db.sql("""delete from `tabItem Barcode`""")
		item_code = "Test Item Barcode"
		if vmraid.db.exists("Item", item_code):
			vmraid.delete_doc("Item", item_code)

		# Create new item and add barcodes
		barcode_properties_list = [
			{
				"barcode": "0012345678905",
				"barcode_type": "EAN"
			},
			{
				"barcode": "012345678905",
				"barcode_type": "UAN"
			},
			{
				"barcode": "ARBITRARY_TEXT",
			}
		]
		create_item(item_code)
		for barcode_properties in barcode_properties_list:
			item_doc = vmraid.get_doc('Item', item_code)
			new_barcode = item_doc.append('barcodes')
			new_barcode.update(barcode_properties)
			item_doc.save()

		# Check values saved correctly
		barcodes = vmraid.get_list(
			'Item Barcode',
			fields=['barcode', 'barcode_type'],
			filters={'parent': item_code})

		for barcode_properties in barcode_properties_list:
			barcode_to_find = barcode_properties['barcode']
			matching_barcodes = [
				x for x in barcodes
				if x['barcode'] == barcode_to_find
			]
		self.assertEqual(len(matching_barcodes), 1)
		details = matching_barcodes[0]

		for key, value in iteritems(barcode_properties):
			self.assertEqual(value, details.get(key))

		# Add barcode again - should cause DuplicateEntryError
		item_doc = vmraid.get_doc('Item', item_code)
		new_barcode = item_doc.append('barcodes')
		new_barcode.update(barcode_properties_list[0])
		self.assertRaises(vmraid.UniqueValidationError, item_doc.save)

		# Add invalid barcode - should cause InvalidBarcode
		item_doc = vmraid.get_doc('Item', item_code)
		new_barcode = item_doc.append('barcodes')
		new_barcode.barcode = '9999999999999'
		new_barcode.barcode_type = 'EAN'
		self.assertRaises(InvalidBarcode, item_doc.save)

def set_item_variant_settings(fields):
	doc = vmraid.get_doc('Item Variant Settings')
	doc.set('fields', fields)
	doc.save()

def make_item_variant():
	if not vmraid.db.exists("Item", "_Test Variant Item-S"):
		variant = create_variant("_Test Variant Item", """{"Test Size": "Small"}""")
		variant.item_code = "_Test Variant Item-S"
		variant.item_name = "_Test Variant Item-S"
		variant.save()

test_records = vmraid.get_test_records('Item')

def create_item(item_code, is_stock_item=None, valuation_rate=0, warehouse=None, is_customer_provided_item=None,
	customer=None, is_purchase_item=None, opening_stock=None, company=None):
	if not vmraid.db.exists("Item", item_code):
		item = vmraid.new_doc("Item")
		item.item_code = item_code
		item.item_name = item_code
		item.description = item_code
		item.item_group = "All Item Groups"
		item.is_stock_item = is_stock_item or 1
		item.opening_stock = opening_stock or 0
		item.valuation_rate = valuation_rate or 0.0
		item.is_purchase_item = is_purchase_item
		item.is_customer_provided_item = is_customer_provided_item
		item.customer = customer or ''
		item.append("item_defaults", {
			"default_warehouse": warehouse or '_Test Warehouse - _TC',
			"company": company or "_Test Company"
		})
		item.save()
	else:
		item = vmraid.get_doc("Item", item_code)
	return item
