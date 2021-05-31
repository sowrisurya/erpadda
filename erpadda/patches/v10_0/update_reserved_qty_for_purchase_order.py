from __future__ import unicode_literals
import vmraid
from erpadda.stock.utils import get_bin

def execute():
	po_item = list(vmraid.db.sql(("""
		select distinct po.name as poname, poitem.rm_item_code as rm_item_code, po.company
		from `tabPurchase Order` po, `tabPurchase Order Item Supplied` poitem
		where po.name = poitem.parent
			and po.is_subcontracted = "Yes"
			and po.docstatus = 1"""), as_dict=1))
	if not po_item:
		return

	vmraid.reload_doc("stock", "doctype", "bin")
	vmraid.reload_doc("buying", "doctype", "purchase_order_item_supplied")
	company_warehouse = vmraid._dict(vmraid.db.sql("""select company, min(name) from `tabWarehouse`
		where is_group = 0 group by company"""))

	items = list(set([d.rm_item_code for d in po_item]))
	item_wh = vmraid._dict(vmraid.db.sql("""select item_code, default_warehouse
		from `tabItem` where name in ({0})""".format(", ".join(["%s"] * len(items))), items))

	# Update reserved warehouse
	for item in po_item:
		reserve_warehouse = get_warehouse(item.rm_item_code, item.company, company_warehouse, item_wh)
		vmraid.db.sql("""update `tabPurchase Order Item Supplied`
			set reserve_warehouse = %s
			where parent = %s and rm_item_code = %s
		""", (reserve_warehouse, item["poname"], item["rm_item_code"]))

	# Update bin
	item_wh_bin = vmraid.db.sql(("""
		select distinct poitemsup.rm_item_code as rm_item_code,
			poitemsup.reserve_warehouse as reserve_warehouse
		from `tabPurchase Order` po, `tabPurchase Order Item Supplied` poitemsup
		where po.name = poitemsup.parent
			and po.is_subcontracted = "Yes"
			and po.docstatus = 1"""), as_dict=1)
	for d in item_wh_bin:
		try:
			stock_bin = get_bin(d["rm_item_code"], d["reserve_warehouse"])
			stock_bin.update_reserved_qty_for_sub_contracting()
		except:
			pass

def get_warehouse(item_code, company, company_warehouse, item_wh):
	reserve_warehouse = item_wh.get(item_code)
	if vmraid.db.get_value("Warehouse", reserve_warehouse, "company") != company:
		reserve_warehouse = None
	if not reserve_warehouse:
		reserve_warehouse = company_warehouse.get(company)
	return reserve_warehouse
