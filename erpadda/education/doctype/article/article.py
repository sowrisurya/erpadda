# -*- coding: utf-8 -*-
# Copyright (c) 2018, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.model.document import Document

class Article(Document):
	def get_article(self):
		pass

@vmraid.whitelist()
def get_topics_without_article(article):
	data = []
	for entry in vmraid.db.get_all('Topic'):
		topic = vmraid.get_doc('Topic', entry.name)
		topic_contents = [tc.content for tc in topic.topic_content]
		if not topic_contents or article not in topic_contents:
			data.append(topic.name)
	return data