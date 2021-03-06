from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc('assets', 'doctype', 'asset')
	vmraid.reload_doc('assets', 'doctype', 'depreciation_schedule')

	vmraid.db.sql("""
		update tabAsset a
		set calculate_depreciation = 1
		where exists(select ds.name from `tabDepreciation Schedule` ds where ds.parent=a.name)
	""")