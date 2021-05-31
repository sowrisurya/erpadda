# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
from __future__ import unicode_literals

import vmraid
import unittest
from vmraid.utils import getdate
from datetime import timedelta


class TestHolidayList(unittest.TestCase):
	def test_holiday_list(self):
		today_date = getdate()
		test_holiday_dates = [today_date-timedelta(days=5), today_date-timedelta(days=4)]
		holiday_list = make_holiday_list("test_holiday_list",
			holiday_dates=[
				{'holiday_date': test_holiday_dates[0], 'description': 'test holiday'},
				{'holiday_date': test_holiday_dates[1], 'description': 'test holiday2'}
			])
		fetched_holiday_list = vmraid.get_value('Holiday List', holiday_list.name)
		self.assertEqual(holiday_list.name, fetched_holiday_list)

def make_holiday_list(name, from_date=getdate()-timedelta(days=10), to_date=getdate(), holiday_dates=None):
	vmraid.delete_doc_if_exists("Holiday List", name, force=1)
	doc = vmraid.get_doc({
		"doctype": "Holiday List",
		"holiday_list_name": name,
		"from_date" : from_date,
		"to_date" : to_date,
		"holidays" : holiday_dates
		}).insert()
	return doc
