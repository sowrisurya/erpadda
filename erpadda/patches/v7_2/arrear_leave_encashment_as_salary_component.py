from __future__ import unicode_literals
import vmraid

def execute():
	# vmraid.reload_doctype('Salary Slip', 'Salary Component')
	vmraid.reload_doc("Payroll", "doctype", "Salary Slip")
	vmraid.reload_doc("Payroll", "doctype", "Salary Component")
	salary_components = [['Arrear', "ARR"], ['Leave Encashment', 'LENC']]
	for salary_component, salary_abbr in salary_components:
		if not vmraid.db.exists('Salary Component', salary_component):
			sal_comp = vmraid.get_doc({
				"doctype": "Salary Component",
				"salary_component": salary_component,
				"type": "Earning",
				"salary_component_abbr": salary_abbr
			}).insert()

	salary_slips = vmraid.db.sql("""select name, arrear_amount, leave_encashment_amount from `tabSalary Slip`
					where docstatus !=2 and (arrear_amount > 0 or leave_encashment_amount > 0)""", as_dict=True)

	for salary_slip in salary_slips:
		doc = vmraid.get_doc('Salary Slip', salary_slip.name)

		if salary_slip.get("arrear_amount") > 0:
			r = doc.append('earnings', {
				'salary_component': 'Arrear',
				'amount': salary_slip.arrear_amount
			})
			r.db_update()

		if salary_slip.get("leave_encashment_amount") > 0:
			r = doc.append('earnings', {
				'salary_component': 'Leave Encashment',
				'amount': salary_slip.leave_encashment_amount
			})
			r.db_update()