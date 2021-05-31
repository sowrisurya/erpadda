# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import vmraid
import vmraid.defaults
from erpadda.shopping_cart.doctype.shopping_cart_settings.shopping_cart_settings import is_cart_enabled

def show_cart_count():
	if (is_cart_enabled() and
		vmraid.db.get_value("User", vmraid.session.user, "user_type") == "Website User"):
		return True

	return False

def set_cart_count(login_manager):
	role, parties = check_customer_or_supplier()
	if role == 'Supplier': return
	if show_cart_count():
		from erpadda.shopping_cart.cart import set_cart_count
		set_cart_count()

def clear_cart_count(login_manager):
	if show_cart_count():
		vmraid.local.cookie_manager.delete_cookie("cart_count")

def update_website_context(context):
	cart_enabled = is_cart_enabled()
	context["shopping_cart_enabled"] = cart_enabled

def check_customer_or_supplier():
	if vmraid.session.user:
		contact_name = vmraid.get_value("Contact", {"email_id": vmraid.session.user})
		if contact_name:
			contact = vmraid.get_doc('Contact', contact_name)
			for link in contact.links:
				if link.link_doctype in ('Customer', 'Supplier'):
					return link.link_doctype, link.link_name

		return 'Customer', None