from __future__ import unicode_literals
import vmraid

def execute():
	if vmraid.db.table_exists("Data Migration Connector"):
		vmraid.db.sql("""
			UPDATE `tabData Migration Connector`
			SET hostname = 'https://hubmarket.org'
			WHERE connector_name = 'Hub Connector'
		""")