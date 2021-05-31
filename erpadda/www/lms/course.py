from __future__ import unicode_literals
import erpadda.education.utils as utils
import vmraid

no_cache = 1

def get_context(context):
	try:
		program = vmraid.form_dict['program']
		course_name = vmraid.form_dict['name']
	except KeyError:
		vmraid.local.flags.redirect_location = '/lms'
		raise vmraid.Redirect

	context.education_settings = vmraid.get_single("Education Settings")
	course = vmraid.get_doc('Course', course_name)
	context.program = program
	context.course = course

	context.topics = course.get_topics()
	context.has_access =  utils.allowed_program_access(context.program)
	context.progress = get_topic_progress(context.topics, course, context.program)

def get_topic_progress(topics, course, program):
	progress = {topic.name: utils.get_topic_progress(topic, course.name, program) for topic in topics}
	return progress
