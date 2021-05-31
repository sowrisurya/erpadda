# -*- coding: utf-8 -*-
# Copyright (c) 2020, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.model.document import Document

class JournalEntryTemplate(Document):
	pass

@vmraid.whitelist()
def get_naming_series():
	return vmraid.get_meta("Journal Entry").get_field("naming_series").options
