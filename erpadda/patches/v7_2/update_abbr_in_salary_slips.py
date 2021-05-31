from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc('Payroll', 'doctype', 'Salary Slip')
	if not vmraid.db.has_column('Salary Detail', 'abbr'):
		return

	salary_details = vmraid.db.sql("""select abbr, salary_component, name from `tabSalary Detail`
				where abbr is null or abbr = ''""", as_dict=True)

	for salary_detail in salary_details:
		salary_component_abbr = vmraid.get_value("Salary Component", salary_detail.salary_component, "salary_component_abbr")
		vmraid.db.sql("""update `tabSalary Detail` set abbr = %s where name = %s""",(salary_component_abbr, salary_detail.name))