# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import unittest
import vmraid
from vmraid.test_runner import make_test_records_for_doctype
from erpadda.stock.get_item_details import get_price_list_rate_for, process_args
from erpadda.stock.doctype.item_price.item_price import ItemPriceDuplicateItem


class TestItemPrice(unittest.TestCase):
	def setUp(self):
		vmraid.db.sql("delete from `tabItem Price`")
		make_test_records_for_doctype("Item Price", force=True)

	def test_duplicate_item(self):
		doc = vmraid.copy_doc(test_records[0])
		self.assertRaises(ItemPriceDuplicateItem, doc.save)

	def test_addition_of_new_fields(self):
		# Based on https://github.com/vmraid/erpadda/issues/8456
		test_fields_existance = [
			'supplier', 'customer', 'uom', 'lead_time_days',
			'packing_unit', 'valid_from', 'valid_upto', 'note'
		]
		doc_fields = vmraid.copy_doc(test_records[1]).__dict__.keys()

		for test_field in test_fields_existance:
			self.assertTrue(test_field in doc_fields)

	def test_dates_validation_error(self):
		doc = vmraid.copy_doc(test_records[1])
		# Enter invalid dates valid_from  >= valid_upto
		doc.valid_from = "2017-04-20"
		doc.valid_upto = "2017-04-17"
		# Valid Upto Date can not be less/equal than Valid From Date
		self.assertRaises(vmraid.ValidationError, doc.save)

	def test_price_in_a_qty(self):
		# Check correct price at this quantity
		doc = vmraid.copy_doc(test_records[2])

		args = {
			"price_list": doc.price_list,
            "customer": doc.customer,
            "uom": "_Test UOM",
            "transaction_date": '2017-04-18',
            "qty": 10
		}

		price = get_price_list_rate_for(process_args(args), doc.item_code)
		self.assertEqual(price, 20.0)

	def test_price_with_no_qty(self):
		# Check correct price when no quantity
		doc = vmraid.copy_doc(test_records[2])
		args = {
			"price_list": doc.price_list,
			"customer": doc.customer,
			"uom": "_Test UOM",
            "transaction_date": '2017-04-18',
		}

		price = get_price_list_rate_for(args, doc.item_code)
		self.assertEqual(price, None)


	def test_prices_at_date(self):
		# Check correct price at first date
		doc = vmraid.copy_doc(test_records[2])

		args = {
			"price_list": doc.price_list,
			"customer": "_Test Customer",
			"uom": "_Test UOM",
			"transaction_date": '2017-04-18',
			"qty": 7
		}

		price = get_price_list_rate_for(args, doc.item_code)
		self.assertEqual(price, 20)

	def test_prices_at_invalid_date(self):
		#Check correct price at invalid date
		doc = vmraid.copy_doc(test_records[3])

		args = {
			"price_list": doc.price_list,
			"qty": 7,
			"uom": "_Test UOM",
			"transaction_date": "01-15-2019"
		}

		price = get_price_list_rate_for(args, doc.item_code)
		self.assertEqual(price, None)

	def test_prices_outside_of_date(self):
		#Check correct price when outside of the date
		doc = vmraid.copy_doc(test_records[4])

		args = {
			"price_list": doc.price_list,
            "customer": "_Test Customer",
            "uom": "_Test UOM",
			"transaction_date": "2017-04-25",
			"qty": 7,
		}

		price = get_price_list_rate_for(args, doc.item_code)
		self.assertEqual(price, None)

	def test_lowest_price_when_no_date_provided(self):
		#Check lowest price when no date provided
		doc = vmraid.copy_doc(test_records[1])

		args = {
			"price_list": doc.price_list,
			"uom": "_Test UOM",
			"qty": 7,
		}

		price = get_price_list_rate_for(args, doc.item_code)
		self.assertEqual(price, 10)


	def test_invalid_item(self):
		doc = vmraid.copy_doc(test_records[1])
		# Enter invalid item code
		doc.item_code = "This is not an item code"
		# Valid item codes must already exist
		self.assertRaises(vmraid.ValidationError, doc.save)

	def test_invalid_price_list(self):
		doc = vmraid.copy_doc(test_records[1])
		# Check for invalid price list
		doc.price_list = "This is not a price list"
		# Valid price list must already exist
		self.assertRaises(vmraid.ValidationError, doc.save)

	def test_empty_duplicate_validation(self):
		# Check if none/empty values are not compared during insert validation
		doc = vmraid.copy_doc(test_records[2])
		doc.customer = None
		doc.price_list_rate = 21
		doc.insert()

		args = {
			"price_list": doc.price_list,
			"uom": "_Test UOM",
			"transaction_date": '2017-04-18',
			"qty": 7
		}

		price = get_price_list_rate_for(args, doc.item_code)
		vmraid.db.rollback()

		self.assertEqual(price, 21)

test_records = vmraid.get_test_records('Item Price')
