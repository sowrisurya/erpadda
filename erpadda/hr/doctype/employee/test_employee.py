# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
from __future__ import unicode_literals


import vmraid
import erpadda
import unittest
import vmraid.utils
from erpadda.hr.doctype.employee.employee import EmployeeLeftValidationError

test_records = vmraid.get_test_records('Employee')

class TestEmployee(unittest.TestCase):
	def test_birthday_reminders(self):
		employee = vmraid.get_doc("Employee", vmraid.db.sql_list("select name from tabEmployee limit 1")[0])
		employee.date_of_birth = "1992" + vmraid.utils.nowdate()[4:]
		employee.company_email = "test@example.com"
		employee.company = "_Test Company"
		employee.save()

		from erpadda.hr.doctype.employee.employee import get_employees_who_are_born_today, send_birthday_reminders

		employees_born_today = get_employees_who_are_born_today()
		self.assertTrue(employees_born_today.get("_Test Company"))

		vmraid.db.sql("delete from `tabEmail Queue`")

		hr_settings = vmraid.get_doc("HR Settings", "HR Settings")
		hr_settings.stop_birthday_reminders = 0
		hr_settings.save()

		send_birthday_reminders()

		email_queue = vmraid.db.sql("""select * from `tabEmail Queue`""", as_dict=True)
		self.assertTrue("Subject: Birthday Reminder" in email_queue[0].message)

	def test_employee_status_left(self):
		employee1 = make_employee("test_employee_1@company.com")
		employee2 = make_employee("test_employee_2@company.com")
		employee1_doc = vmraid.get_doc("Employee", employee1)
		employee2_doc = vmraid.get_doc("Employee", employee2)
		employee2_doc.reload()
		employee2_doc.reports_to = employee1_doc.name
		employee2_doc.save()
		employee1_doc.reload()
		employee1_doc.status = 'Left'
		self.assertRaises(EmployeeLeftValidationError, employee1_doc.save)

def make_employee(user, company=None, **kwargs):
	""
	if not vmraid.db.get_value("User", user):
		vmraid.get_doc({
			"doctype": "User",
			"email": user,
			"first_name": user,
			"new_password": "password",
			"roles": [{"doctype": "Has Role", "role": "Employee"}]
		}).insert()

	if not vmraid.db.get_value("Employee", {"user_id": user}):
		employee = vmraid.get_doc({
			"doctype": "Employee",
			"naming_series": "EMP-",
			"first_name": user,
			"company": company or erpadda.get_default_company(),
			"user_id": user,
			"date_of_birth": "1990-05-08",
			"date_of_joining": "2013-01-01",
			"department": vmraid.get_all("Department", fields="name")[0].name,
			"gender": "Female",
			"company_email": user,
			"prefered_contact_email": "Company Email",
			"prefered_email": user,
			"status": "Active",
			"employment_type": "Intern"
		})
		if kwargs:
			employee.update(kwargs)
		employee.insert()
		return employee.name
	else:
		return vmraid.get_value("Employee", {"employee_name":user}, "name")
