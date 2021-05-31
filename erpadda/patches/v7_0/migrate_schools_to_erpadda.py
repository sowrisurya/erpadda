from __future__ import unicode_literals
import vmraid, os
from vmraid.installer import remove_from_installed_apps

def execute():
	reload_doctypes_for_schools_icons()

	vmraid.reload_doc('website', 'doctype', 'portal_settings')
	vmraid.reload_doc('website', 'doctype', 'portal_menu_item')
	vmraid.reload_doc('buying', 'doctype', 'request_for_quotation')

	if 'schools' in vmraid.get_installed_apps():
		if not vmraid.db.exists('Module Def', 'Schools') and vmraid.db.exists('Module Def', 'Academics'):

			# 'Schools' module changed to the 'Education'
			# vmraid.rename_doc("Module Def", "Academics", "Schools")

			vmraid.rename_doc("Module Def", "Academics", "Education")

		remove_from_installed_apps("schools")

def reload_doctypes_for_schools_icons():
	# 'Schools' module changed to the 'Education'
	# base_path = vmraid.get_app_path('erpadda', 'schools', 'doctype')

	base_path = vmraid.get_app_path('erpadda', 'education', 'doctype')
	for doctype in os.listdir(base_path):
		if os.path.exists(os.path.join(base_path, doctype, doctype + '.json')) \
			and doctype not in ("fee_component", "assessment", "assessment_result"):
			vmraid.reload_doc('education', 'doctype', doctype)