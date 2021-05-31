from __future__ import unicode_literals
import vmraid

def get_context(context):
	context.no_cache = True
	chapter = vmraid.get_doc('Chapter', vmraid.form_dict.name)
	context.member_deleted = True
	context.chapter = chapter
