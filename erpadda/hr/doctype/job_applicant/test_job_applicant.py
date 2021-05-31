# -*- coding: utf-8 -*-
# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors and Contributors
# See license.txt
from __future__ import unicode_literals

import vmraid
import unittest

# test_records = vmraid.get_test_records('Job Applicant')

class TestJobApplicant(unittest.TestCase):
	pass

def create_job_applicant(**args):
	args = vmraid._dict(args)

	filters = {
		"applicant_name": args.applicant_name or "_Test Applicant",
		"email_id": args.email_id or "test_applicant@example.com",
	}

	if vmraid.db.exists("Job Applicant", filters):
		return vmraid.get_doc("Job Applicant", filters)

	job_applicant = vmraid.get_doc({
		"doctype": "Job Applicant",
		"status": args.status or "Open"
	})

	job_applicant.update(filters)
	job_applicant.save()

	return job_applicant
