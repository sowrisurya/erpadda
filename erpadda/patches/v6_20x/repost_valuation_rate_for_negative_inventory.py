# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.utils import cint
from erpadda.stock.stock_balance import repost

def execute():
	if cint(vmraid.db.get_value("Stock Settings", None, "allow_negative_stock")):
		repost(only_actual=True)