from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype("Purchase Order")
	vmraid.reload_doctype("Purchase Order Item")

	if not vmraid.db.has_column("Purchase Order", "delivered_by_supplier"):
		return

	for po in vmraid.get_all("Purchase Order", filters={"delivered_by_supplier": 1}, fields=["name"]):
		purchase_order = vmraid.get_doc("Purchase Order", po)

		for item in purchase_order.items:
			if item.prevdoc_doctype == "Sales Order":
				delivered_by_supplier = vmraid.get_value("Sales Order Item", item.prevdoc_detail_docname,
					"delivered_by_supplier")

				if delivered_by_supplier:
					vmraid.db.sql("""update `tabPurchase Order Item`
						set delivered_by_supplier=1, billed_amt=amount, received_qty=qty
						where name=%s """, item.name)

		update_per_received(purchase_order)
		update_per_billed(purchase_order)

def update_per_received(po):
	vmraid.db.sql(""" update `tabPurchase Order`
				set per_received = round((select sum(if(qty > ifnull(received_qty, 0),
					ifnull(received_qty, 0), qty)) / sum(qty) *100
				from `tabPurchase Order Item`
				where parent = %(name)s), 2)
			where name = %(name)s """, {"name": po.name})

def update_per_billed(po):
	vmraid.db.sql(""" update `tabPurchase Order`
				set per_billed = round((select sum( if(amount > ifnull(billed_amt, 0),
					ifnull(billed_amt, 0), amount)) / sum(amount) *100
				from `tabPurchase Order Item`
				where parent = %(name)s), 2)
			where name = %(name)s """, {"name": po.name})


