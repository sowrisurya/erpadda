# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
from __future__ import unicode_literals

no_cache = 1

import vmraid
from erpadda.shopping_cart.cart import get_cart_quotation

def get_context(context):
	context.update(get_cart_quotation())
