from __future__ import unicode_literals
import vmraid

from vmraid import _

def get_context(context):
	context.no_cache = 1

	timelog = vmraid.get_doc('Time Log', vmraid.form_dict.timelog)
	
	context.doc = timelog