# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	# rename the School module as Education

	# rename the school module
	if vmraid.db.exists('Module Def', 'Schools') and not vmraid.db.exists('Module Def', 'Education'):
		vmraid.rename_doc("Module Def", "Schools", "Education")

	# delete the school module
	if vmraid.db.exists('Module Def', 'Schools') and vmraid.db.exists('Module Def', 'Education'):
		vmraid.db.sql("""delete from `tabModule Def` where module_name = 'Schools'""")


	# rename "School Settings" to the "Education Settings
	if vmraid.db.exists('DocType', 'School Settings'):
		vmraid.rename_doc("DocType", "School Settings", "Education Settings", force=True)
		vmraid.reload_doc("education", "doctype", "education_settings")

	# delete the discussion web form if exists
	if vmraid.db.exists('Web Form', 'Discussion'):
		vmraid.db.sql("""delete from `tabWeb Form` where name = 'discussion'""")

	# rename the select option field from "School Bus" to "Institute's Bus"
	vmraid.reload_doc("education", "doctype", "Program Enrollment")
	if "mode_of_transportation" in vmraid.db.get_table_columns("Program Enrollment"):
		vmraid.db.sql("""update `tabProgram Enrollment` set mode_of_transportation = "Institute's Bus"
			where mode_of_transportation = "School Bus" """)
