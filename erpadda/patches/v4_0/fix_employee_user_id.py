# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import vmraid
from vmraid.utils import get_fullname

def execute():
	for user_id in vmraid.db.sql_list("""select distinct user_id from `tabEmployee`
		where ifnull(user_id, '')!=''
		group by user_id having count(name) > 1"""):

		fullname = get_fullname(user_id)
		employee = vmraid.db.get_value("Employee", {"employee_name": fullname, "user_id": user_id})

		if employee:
			vmraid.db.sql("""update `tabEmployee` set user_id=null
				where user_id=%s and name!=%s""", (user_id, employee))
		else:
			count = vmraid.db.sql("""select count(*) from `tabEmployee` where user_id=%s""", user_id)[0][0]
			vmraid.db.sql("""update `tabEmployee` set user_id=null
				where user_id=%s limit %s""", (user_id, count - 1))
