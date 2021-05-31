from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc('accounts', 'doctype', 'sales_invoice_timesheet')
	vmraid.reload_doc('accounts', 'doctype', 'sales_invoice_payment')
	vmraid.reload_doc('accounts', 'doctype', 'mode_of_payment')

	count = 0
	for data in vmraid.db.sql("""select name, mode_of_payment, cash_bank_account, paid_amount, company 
		from `tabSales Invoice` si
		where si.is_pos = 1 and si.docstatus < 2 
		and si.cash_bank_account is not null and si.cash_bank_account != ''
		and not exists(select name from `tabSales Invoice Payment` where parent=si.name)""", as_dict=1):
		
		if not data.mode_of_payment and not vmraid.db.exists("Mode of Payment", "Cash"):
			mop = vmraid.new_doc("Mode of Payment")
			mop.mode_of_payment = "Cash"
			mop.type = "Cash"
			mop.save()
		
		si_doc = vmraid.get_doc('Sales Invoice', data.name)
		row = si_doc.append('payments', {
			'mode_of_payment': data.mode_of_payment or 'Cash',
			'account': data.cash_bank_account,
			'type': vmraid.db.get_value('Mode of Payment', data.mode_of_payment, 'type') or 'Cash',
			'amount': data.paid_amount
		})
		row.db_update()
		
		si_doc.set_paid_amount()
		si_doc.db_set("paid_amount", si_doc.paid_amount, update_modified = False)
		si_doc.db_set("base_paid_amount", si_doc.base_paid_amount, update_modified = False)
		
		count +=1
		
		if count % 200 == 0:
			vmraid.db.commit()