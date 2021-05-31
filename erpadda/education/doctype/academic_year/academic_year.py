# -*- coding: utf-8 -*-
# Copyright (c) 2015, VMRaid Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid import msgprint, _
from vmraid.model.document import Document

class AcademicYear(Document):
    def validate(self):
        #Check that start of academic year is earlier than end of academic year
        if self.year_start_date and self.year_end_date and self.year_start_date > self.year_end_date:
            vmraid.throw(_("The Year End Date cannot be earlier than the Year Start Date. Please correct the dates and try again."))
