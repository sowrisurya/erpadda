# Copyright (c) 2018, VMRaid Technologies Pvt. Ltd. and Contributors and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid, requests, json, time

from vmraid.model.document import Document
from vmraid.utils import add_years, now, get_datetime, get_datetime_str, cint
from vmraid import _
from vmraid.vmraidclient import VMRaidClient
from erpadda.utilities.product import get_price, get_qty_in_stock
from six import string_types

class MarketplaceSettings(Document):

	def register_seller(self, company, company_description):

		country, currency, company_logo = vmraid.db.get_value('Company', company,
			['country', 'default_currency', 'company_logo'])

		company_details = {
			'company': company,
			'country': country,
			'currency': currency,
			'company_description': company_description,
			'company_logo': company_logo,
			'site_name': vmraid.utils.get_url()
		}

		hub_connection = self.get_connection()

		response = hub_connection.post_request({
			'cmd': 'hub.hub.api.add_hub_seller',
			'company_details': json.dumps(company_details)
		})

		return response


	def add_hub_user(self, user_email):
		'''Create a Hub User and User record on hub server
		and if successfull append it to Hub User table
		'''

		if not self.registered:
			return

		hub_connection = self.get_connection()

		first_name, last_name = vmraid.db.get_value('User', user_email, ['first_name', 'last_name'])

		hub_user = hub_connection.post_request({
			'cmd': 'hub.hub.api.add_hub_user',
			'user_email': user_email,
			'first_name': first_name,
			'last_name': last_name,
			'hub_seller': self.hub_seller_name
		})

		self.append('users', {
			'user': hub_user.get('user_email'),
			'hub_user_name': hub_user.get('hub_user_name'),
			'password': hub_user.get('password')
		})

		self.save()

	def get_hub_user(self, user):
		'''Return the Hub User doc from the `users` table if password is set'''

		filtered_users = list(filter(
			lambda x: x.user == user and x.password,
			self.users
		))

		if filtered_users:
			return filtered_users[0]


	def get_connection(self):
		return VMRaidClient(self.marketplace_url)


	def unregister(self):
		"""Disable the User on hubmarket.org"""
		pass

@vmraid.whitelist()
def is_marketplace_enabled():
	if not hasattr(vmraid.local, 'is_marketplace_enabled'):
		vmraid.local.is_marketplace_enabled = cint(vmraid.db.get_single_value('Marketplace Settings',
			'disable_marketplace'))

	return vmraid.local.is_marketplace_enabled
