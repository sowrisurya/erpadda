# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
from __future__ import unicode_literals


import vmraid, unittest
from erpadda.accounts.party import get_due_date
from erpadda.exceptions import PartyDisabled
from vmraid.test_runner import make_test_records

test_dependencies = ['Payment Term', 'Payment Terms Template']
test_records = vmraid.get_test_records('Supplier')


class TestSupplier(unittest.TestCase):
    def test_supplier_default_payment_terms(self):
        # Payment Term based on Days after invoice date
        vmraid.db.set_value(
            "Supplier", "_Test Supplier With Template 1", "payment_terms", "_Test Payment Term Template 3")

        due_date = get_due_date("2016-01-22", "Supplier", "_Test Supplier With Template 1")
        self.assertEqual(due_date, "2016-02-21")

        due_date = get_due_date("2017-01-22", "Supplier", "_Test Supplier With Template 1")
        self.assertEqual(due_date, "2017-02-21")

        # Payment Term based on last day of month
        vmraid.db.set_value(
            "Supplier", "_Test Supplier With Template 1", "payment_terms", "_Test Payment Term Template 1")

        due_date = get_due_date("2016-01-22", "Supplier", "_Test Supplier With Template 1")
        self.assertEqual(due_date, "2016-02-29")

        due_date = get_due_date("2017-01-22", "Supplier", "_Test Supplier With Template 1")
        self.assertEqual(due_date, "2017-02-28")

        vmraid.db.set_value("Supplier", "_Test Supplier With Template 1", "payment_terms", "")

        # Set credit limit for the supplier group instead of supplier and evaluate the due date
        vmraid.db.set_value("Supplier Group", "_Test Supplier Group", "payment_terms", "_Test Payment Term Template 3")

        due_date = get_due_date("2016-01-22", "Supplier", "_Test Supplier With Template 1")
        self.assertEqual(due_date, "2016-02-21")

        # Payment terms for Supplier Group instead of supplier and evaluate the due date
        vmraid.db.set_value("Supplier Group", "_Test Supplier Group", "payment_terms", "_Test Payment Term Template 1")

        # Leap year
        due_date = get_due_date("2016-01-22", "Supplier", "_Test Supplier With Template 1")
        self.assertEqual(due_date, "2016-02-29")
        # # Non Leap year
        due_date = get_due_date("2017-01-22", "Supplier", "_Test Supplier With Template 1")
        self.assertEqual(due_date, "2017-02-28")

        # Supplier with no default Payment Terms Template
        vmraid.db.set_value("Supplier Group", "_Test Supplier Group", "payment_terms", "")
        vmraid.db.set_value("Supplier", "_Test Supplier", "payment_terms", "")

        due_date = get_due_date("2016-01-22", "Supplier", "_Test Supplier")
        self.assertEqual(due_date, "2016-01-22")
        # # Non Leap year
        due_date = get_due_date("2017-01-22", "Supplier", "_Test Supplier")
        self.assertEqual(due_date, "2017-01-22")

    def test_supplier_disabled(self):
        make_test_records("Item")

        vmraid.db.set_value("Supplier", "_Test Supplier", "disabled", 1)

        from erpadda.buying.doctype.purchase_order.test_purchase_order import create_purchase_order

        po = create_purchase_order(do_not_save=True)

        self.assertRaises(PartyDisabled, po.save)

        vmraid.db.set_value("Supplier", "_Test Supplier", "disabled", 0)

        po.save()

    def test_supplier_country(self):
        # Test that country field exists in Supplier DocType
        supplier = vmraid.get_doc('Supplier', '_Test Supplier with Country')
        self.assertTrue('country' in supplier.as_dict())

        # Test if test supplier field record is 'Greece'
        self.assertEqual(supplier.country, "Greece")

        # Test update Supplier instance country value
        supplier = vmraid.get_doc('Supplier', '_Test Supplier')
        supplier.country = 'Greece'
        supplier.save()
        self.assertEqual(supplier.country, "Greece")

    def test_party_details_tax_category(self):
        from erpadda.accounts.party import get_party_details

        vmraid.delete_doc_if_exists("Address", "_Test Address With Tax Category-Billing")

        # Tax Category without Address
        details = get_party_details("_Test Supplier With Tax Category", party_type="Supplier")
        self.assertEqual(details.tax_category, "_Test Tax Category 1")

        address = vmraid.get_doc(dict(
            doctype='Address',
            address_title='_Test Address With Tax Category',
            tax_category='_Test Tax Category 2',
            address_type='Billing',
            address_line1='Station Road',
            city='_Test City',
            country='India',
            links=[dict(
                link_doctype='Supplier',
                link_name='_Test Supplier With Tax Category'
            )]
        )).insert()

        # Tax Category with Address
        details = get_party_details("_Test Supplier With Tax Category", party_type="Supplier")
        self.assertEqual(details.tax_category, "_Test Tax Category 2")

        # Rollback
        address.delete()

def create_supplier(**args):
    args = vmraid._dict(args)

    try:
        doc = vmraid.get_doc({
            "doctype": "Supplier",
            "supplier_name": args.supplier_name,
            "supplier_group": args.supplier_group or "Services",
            "supplier_type": args.supplier_type or "Company",
            "tax_withholding_category": args.tax_withholding_category
        }).insert()

        return doc

    except vmraid.DuplicateEntryError:
        return vmraid.get_doc("Supplier", args.supplier_name)