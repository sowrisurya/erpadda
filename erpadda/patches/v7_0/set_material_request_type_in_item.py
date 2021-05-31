from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype("Item")
	if "default_bom" in vmraid.db.get_table_columns("Item"):
		vmraid.db.sql("""update `tabItem` 
			set default_material_request_type = (
				case 
					when (default_bom is not null and default_bom != '')
					then 'Manufacture' 
					else 'Purchase' 
				end )""")
				
	else:
		vmraid.db.sql("update tabItem set default_material_request_type='Purchase'")