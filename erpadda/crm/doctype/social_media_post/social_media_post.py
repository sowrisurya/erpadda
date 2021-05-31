# -*- coding: utf-8 -*-
# Copyright (c) 2020, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.model.document import Document
from vmraid import _
import datetime

class SocialMediaPost(Document):
	def validate(self):
		if self.scheduled_time:
			current_time = vmraid.utils.now_datetime()
			scheduled_time = vmraid.utils.get_datetime(self.scheduled_time)
			if scheduled_time < current_time:
				vmraid.throw(_("Invalid Scheduled Time"))

	def submit(self):
		if self.scheduled_time:
			self.post_status = "Scheduled"
		super(SocialMediaPost, self).submit()

	def post(self):
		try:
			if self.twitter and not self.twitter_post_id:
				twitter = vmraid.get_doc("Twitter Settings")
				twitter_post = twitter.post(self.text, self.image)
				self.db_set("twitter_post_id", twitter_post.id)
			if self.linkedin and not self.linkedin_post_id:
				linkedin = vmraid.get_doc("LinkedIn Settings")
				linkedin_post = linkedin.post(self.linkedin_post, self.image)
				self.db_set("linkedin_post_id", linkedin_post.headers['X-RestLi-Id'].split(":")[-1])
			self.db_set("post_status", "Posted")

		except:
			self.db_set("post_status", "Error")
			title = _("Error while POSTING {0}").format(self.name)
			traceback = vmraid.get_traceback()
			vmraid.log_error(message=traceback , title=title)

def process_scheduled_social_media_posts():
	posts = vmraid.get_list("Social Media Post", filters={"post_status": "Scheduled", "docstatus":1}, fields= ["name", "scheduled_time","post_status"])
	start = vmraid.utils.now_datetime()
	end = start + datetime.timedelta(minutes=10)
	for post in posts:
		if post.scheduled_time:
			post_time = vmraid.utils.get_datetime(post.scheduled_time)
			if post_time > start and post_time <= end:
				publish('Social Media Post', post.name)

@vmraid.whitelist()
def publish(doctype, name):
	sm_post = vmraid.get_doc(doctype, name)
	sm_post.post()
	vmraid.db.commit()
