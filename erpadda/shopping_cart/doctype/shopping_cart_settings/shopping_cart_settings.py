# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid import _, msgprint
from vmraid.utils import comma_and
from vmraid.model.document import Document
from vmraid.utils import get_datetime, get_datetime_str, now_datetime

class ShoppingCartSetupError(vmraid.ValidationError): pass

class ShoppingCartSettings(Document):
	def onload(self):
		self.get("__onload").quotation_series = vmraid.get_meta("Quotation").get_options("naming_series")

	def validate(self):
		if self.enabled:
			self.validate_exchange_rates_exist()

	def validate_exchange_rates_exist(self):
		"""check if exchange rates exist for all Price List currencies (to company's currency)"""
		company_currency = vmraid.get_cached_value('Company',  self.company,  "default_currency")
		if not company_currency:
			msgprint(_("Please specify currency in Company") + ": " + self.company,
				raise_exception=ShoppingCartSetupError)

		price_list_currency_map = vmraid.db.get_values("Price List",
			[self.price_list], "currency")

		price_list_currency_map = dict(price_list_currency_map)
		
		# check if all price lists have a currency
		for price_list, currency in price_list_currency_map.items():
			if not currency:
				vmraid.throw(_("Currency is required for Price List {0}").format(price_list))

		expected_to_exist = [currency + "-" + company_currency
			for currency in price_list_currency_map.values()
			if currency != company_currency]

		# manqala 20/09/2016: set up selection parameters for query from tabCurrency Exchange
		from_currency = [currency for currency in price_list_currency_map.values() if currency != company_currency]
		to_currency = company_currency
		# manqala end

		if expected_to_exist:
			# manqala 20/09/2016: modify query so that it uses date in the selection from Currency Exchange.
			# exchange rates defined with date less than the date on which this document is being saved will be selected
			exists = vmraid.db.sql_list("""select CONCAT(from_currency,'-',to_currency) from `tabCurrency Exchange`
				where from_currency in (%s) and to_currency = "%s" and date <= curdate()""" % (", ".join(["%s"]*len(from_currency)), to_currency), tuple(from_currency))
			# manqala end

			missing = list(set(expected_to_exist).difference(exists))

			if missing:
				msgprint(_("Missing Currency Exchange Rates for {0}").format(comma_and(missing)),
					raise_exception=ShoppingCartSetupError)

	def validate_tax_rule(self):
		if not vmraid.db.get_value("Tax Rule", {"use_for_shopping_cart" : 1}, "name"):
			vmraid.throw(vmraid._("Set Tax Rule for shopping cart"), ShoppingCartSetupError)

	def get_tax_master(self, billing_territory):
		tax_master = self.get_name_from_territory(billing_territory, "sales_taxes_and_charges_masters",
			"sales_taxes_and_charges_master")
		return tax_master and tax_master[0] or None

	def get_shipping_rules(self, shipping_territory):
		return self.get_name_from_territory(shipping_territory, "shipping_rules", "shipping_rule")

def validate_cart_settings(doc, method):
	vmraid.get_doc("Shopping Cart Settings", "Shopping Cart Settings").run_method("validate")

def get_shopping_cart_settings():
	if not getattr(vmraid.local, "shopping_cart_settings", None):
		vmraid.local.shopping_cart_settings = vmraid.get_doc("Shopping Cart Settings", "Shopping Cart Settings")

	return vmraid.local.shopping_cart_settings

@vmraid.whitelist(allow_guest=True)
def is_cart_enabled():
	return get_shopping_cart_settings().enabled

def show_quantity_in_website():
	return get_shopping_cart_settings().show_quantity_in_website

def check_shopping_cart_enabled():
	if not get_shopping_cart_settings().enabled:
		vmraid.throw(_("You need to enable Shopping Cart"), ShoppingCartSetupError)

def show_attachments():
	return get_shopping_cart_settings().show_attachments
