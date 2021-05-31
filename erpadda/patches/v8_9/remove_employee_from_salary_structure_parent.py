from __future__ import unicode_literals
import vmraid

def execute():
	if 'employee' in vmraid.db.get_table_columns("Salary Structure"):
		vmraid.db.sql("alter table `tabSalary Structure` drop column employee")
