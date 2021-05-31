from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc("website", "doctype", "contact_us_settings")
	address = vmraid.db.get_value("Contact Us Settings", None, "address")
	if address:
		address = vmraid.get_doc("Address", address)
		contact = vmraid.get_doc("Contact Us Settings", "Contact Us Settings")
		for f in ("address_title", "address_line1", "address_line2", "city", "state", "country", "pincode"):
			contact.set(f, address.get(f))
		
		contact.save()