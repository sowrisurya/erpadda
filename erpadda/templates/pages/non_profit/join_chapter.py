from __future__ import unicode_literals
import vmraid

def get_context(context):
	context.no_cache = True
	chapter = vmraid.get_doc('Chapter', vmraid.form_dict.name)
	if vmraid.session.user!='Guest':
		if vmraid.session.user in [d.user for d in chapter.members if d.enabled == 1]:
			context.already_member = True
		else:
			if vmraid.request.method=='GET':
				pass
			elif vmraid.request.method=='POST':
				chapter.append('members', dict(
					user=vmraid.session.user,
					introduction=vmraid.form_dict.introduction,
					website_url=vmraid.form_dict.website_url,
					enabled=1
				))
				chapter.save(ignore_permissions=1)
				vmraid.db.commit()

	context.chapter = chapter
