from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.delete_doc_if_exists("DocType", "BOM Replace Tool")

	vmraid.reload_doctype("BOM")
	vmraid.db.sql("update tabBOM set conversion_rate=1 where conversion_rate is null or conversion_rate=0")
	vmraid.db.sql("update tabBOM set set_rate_of_sub_assembly_item_based_on_bom=1")