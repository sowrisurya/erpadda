from __future__ import unicode_literals
import vmraid
from vmraid.utils import flt

def execute():
	vmraid.reload_doc('Payroll', 'doctype', 'salary_component')
	sal_components = vmraid.db.sql("""
		select DISTINCT salary_component, parentfield from `tabSalary Detail`""", as_dict=True)

	if sal_components:
		for sal_component in sal_components:
			if sal_component.parentfield == "earnings":
				vmraid.db.sql("""update `tabSalary Component` set type='Earning' where salary_component=%(sal_comp)s""",{"sal_comp": sal_component.salary_component})
			else:
				vmraid.db.sql("""update `tabSalary Component` set type='Deduction' where salary_component=%(sal_comp)s""",{"sal_comp": sal_component.salary_component})