from __future__ import unicode_literals
import vmraid
from vmraid.custom.doctype.property_setter.property_setter import make_property_setter, delete_property_setter

def execute():
	vmraid.reload_doc("projects", "doctype", "project")

	vmraid.db.sql("""UPDATE `tabProject`
		SET
			naming_series = 'PROJ-.####'
		WHERE
			naming_series is NULL""")

