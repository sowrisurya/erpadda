from __future__ import unicode_literals

import vmraid
from vmraid import _

no_cache = 1

def get_context(context):
	if vmraid.session.user=='Guest':
		vmraid.throw(_("You need to be logged in to access this page"), vmraid.PermissionError)

	context.show_sidebar=True

	if vmraid.db.exists("Patient", {'email': vmraid.session.user}):
		patient = vmraid.get_doc("Patient", {'email': vmraid.session.user})
		context.doc = patient
		vmraid.form_dict.new = 0
		vmraid.form_dict.name = patient.name

def get_patient():
	return vmraid.get_value("Patient",{"email": vmraid.session.user}, "name")

def has_website_permission(doc, ptype, user, verbose=False):
	if doc.name == get_patient():
		return True
	else:
		return False
