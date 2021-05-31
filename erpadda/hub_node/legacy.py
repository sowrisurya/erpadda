from __future__ import unicode_literals
import vmraid, json
from vmraid.utils import nowdate
from vmraid.vmraidclient import VMRaidClient
from vmraid.utils.nestedset import get_root_of
from vmraid.contacts.doctype.contact.contact import get_default_contact

def get_list(doctype, start, limit, fields, filters, order_by):
	pass

def get_hub_connection():
	if vmraid.db.exists('Data Migration Connector', 'Hub Connector'):
		hub_connector = vmraid.get_doc('Data Migration Connector', 'Hub Connector')
		hub_connection = hub_connector.get_connection()
		return hub_connection.connection

	# read-only connection
	hub_connection = VMRaidClient(vmraid.conf.hub_url)
	return hub_connection

def make_opportunity(buyer_name, email_id):
	buyer_name = "HUB-" + buyer_name

	if not vmraid.db.exists('Lead', {'email_id': email_id}):
		lead = vmraid.new_doc("Lead")
		lead.lead_name = buyer_name
		lead.email_id = email_id
		lead.save(ignore_permissions=True)

	o = vmraid.new_doc("Opportunity")
	o.opportunity_from = "Lead"
	o.lead = vmraid.get_all("Lead", filters={"email_id": email_id}, fields = ["name"])[0]["name"]
	o.save(ignore_permissions=True)

@vmraid.whitelist()
def make_rfq_and_send_opportunity(item, supplier):
	supplier = make_supplier(supplier)
	contact = make_contact(supplier)
	item = make_item(item)
	rfq = make_rfq(item, supplier, contact)
	status = send_opportunity(contact)

	return {
		'rfq': rfq,
		'hub_document_created': status
	}

def make_supplier(supplier):
	# make supplier if not already exists
	supplier = vmraid._dict(json.loads(supplier))

	if not vmraid.db.exists('Supplier', {'supplier_name': supplier.supplier_name}):
		supplier_doc = vmraid.get_doc({
			'doctype': 'Supplier',
			'supplier_name': supplier.supplier_name,
			'supplier_group': supplier.supplier_group,
			'supplier_email': supplier.supplier_email
		}).insert()
	else:
		supplier_doc = vmraid.get_doc('Supplier', supplier.supplier_name)

	return supplier_doc

def make_contact(supplier):
	contact_name = get_default_contact('Supplier', supplier.supplier_name)
	# make contact if not already exists
	if not contact_name:
		contact = vmraid.get_doc({
			'doctype': 'Contact',
			'first_name': supplier.supplier_name,
			'is_primary_contact': 1,
			'links': [
				{'link_doctype': 'Supplier', 'link_name': supplier.supplier_name}
			]
		})
		contact.add_email(supplier.supplier_email, is_primary=True)
		contact.insert()
	else:
		contact = vmraid.get_doc('Contact', contact_name)

	return contact

def make_item(item):
	# make item if not already exists
	item = vmraid._dict(json.loads(item))

	if not vmraid.db.exists('Item', {'item_code': item.item_code}):
		item_doc = vmraid.get_doc({
			'doctype': 'Item',
			'item_code': item.item_code,
			'item_group': item.item_group,
			'is_item_from_hub': 1
		}).insert()
	else:
		item_doc = vmraid.get_doc('Item', item.item_code)

	return item_doc

def make_rfq(item, supplier, contact):
	# make rfq
	rfq = vmraid.get_doc({
		'doctype': 'Request for Quotation',
		'transaction_date': nowdate(),
		'status': 'Draft',
		'company': vmraid.db.get_single_value('Marketplace Settings', 'company'),
		'message_for_supplier': 'Please supply the specified items at the best possible rates',
		'suppliers': [
			{ 'supplier': supplier.name, 'contact': contact.name }
		],
		'items': [
			{
				'item_code': item.item_code,
				'qty': 1,
				'schedule_date': nowdate(),
				'warehouse': item.default_warehouse or get_root_of("Warehouse"),
				'description': item.description,
				'uom': item.stock_uom
			}
		]
	}).insert()

	rfq.save()
	rfq.submit()
	return rfq

def send_opportunity(contact):
	# Make Hub Message on Hub with lead data
	doc = {
		'doctype': 'Lead',
		'lead_name': vmraid.db.get_single_value('Marketplace Settings', 'company'),
		'email_id': vmraid.db.get_single_value('Marketplace Settings', 'user')
	}

	args = vmraid._dict(dict(
		doctype='Hub Message',
		reference_doctype='Lead',
		data=json.dumps(doc),
		user=contact.email_id
	))

	connection = get_hub_connection()
	response = connection.insert('Hub Message', args)

	return response.ok
