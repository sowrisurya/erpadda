# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	""" 
		disable the instructor role for companies with domain other than
		Education.
	"""

	domains = vmraid.db.sql_list("select domain from tabCompany")
	if "Education" not in domains:
		if vmraid.db.exists("Role", "Instructor"):
			role = vmraid.get_doc("Role", "Instructor")
			role.disabled = 1
			role.save(ignore_permissions=True)