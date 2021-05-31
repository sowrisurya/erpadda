# -*- coding: utf-8 -*-
# Copyright (c) 2018, VMRaid Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import vmraid
import unittest
from vmraid.utils import nowdate
from erpadda.hr.doctype.employee_onboarding.employee_onboarding import make_employee
from erpadda.hr.doctype.employee_onboarding.employee_onboarding import IncompleteTaskError
from erpadda.hr.doctype.job_offer.test_job_offer import create_job_offer

class TestEmployeeOnboarding(unittest.TestCase):
	def test_employee_onboarding_incomplete_task(self):
		if vmraid.db.exists('Employee Onboarding', {'employee_name': 'Test Researcher'}):
			vmraid.delete_doc('Employee Onboarding', {'employee_name': 'Test Researcher'})
		_set_up()
		applicant = get_job_applicant()

		job_offer = create_job_offer(job_applicant=applicant.name)
		job_offer.submit()

		onboarding = vmraid.new_doc('Employee Onboarding')
		onboarding.job_applicant = applicant.name
		onboarding.job_offer = job_offer.name
		onboarding.company = '_Test Company'
		onboarding.designation = 'Researcher'
		onboarding.append('activities', {
			'activity_name': 'Assign ID Card',
			'role': 'HR User',
			'required_for_employee_creation': 1
		})
		onboarding.append('activities', {
			'activity_name': 'Assign a laptop',
			'role': 'HR User'
		})
		onboarding.status = 'Pending'
		onboarding.insert()
		onboarding.submit()

		project_name = vmraid.db.get_value("Project", onboarding.project, "project_name")
		self.assertEqual(project_name, 'Employee Onboarding : Test Researcher - test@researcher.com')

		# don't allow making employee if onboarding is not complete
		self.assertRaises(IncompleteTaskError, make_employee, onboarding.name)

		# complete the task
		project = vmraid.get_doc('Project', onboarding.project)
		for task in vmraid.get_all('Task', dict(project=project.name)):
			task = vmraid.get_doc('Task', task.name)
			task.status = 'Completed'
			task.save()

		# make employee
		onboarding.reload()
		employee = make_employee(onboarding.name)
		employee.first_name = employee.employee_name
		employee.date_of_joining = nowdate()
		employee.date_of_birth = '1990-05-08'
		employee.gender = 'Female'
		employee.insert()
		self.assertEqual(employee.employee_name, 'Test Researcher')

def get_job_applicant():
	if vmraid.db.exists('Job Applicant', 'Test Researcher - test@researcher.com'):
		return vmraid.get_doc('Job Applicant', 'Test Researcher - test@researcher.com')
	applicant = vmraid.new_doc('Job Applicant')
	applicant.applicant_name = 'Test Researcher'
	applicant.email_id = 'test@researcher.com'
	applicant.status = 'Open'
	applicant.cover_letter = 'I am a great Researcher.'
	applicant.insert()
	return applicant

def _set_up():
	for doctype in ["Employee Onboarding"]:
		vmraid.db.sql("delete from `tab{doctype}`".format(doctype=doctype))

	project = "Employee Onboarding : Test Researcher - test@researcher.com"
	vmraid.db.sql("delete from tabProject where name=%s", project)
	vmraid.db.sql("delete from tabTask where project=%s", project)