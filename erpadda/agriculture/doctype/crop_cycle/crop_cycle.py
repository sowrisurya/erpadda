# -*- coding: utf-8 -*-
# Copyright (c) 2017, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import ast

import vmraid
from vmraid import _
from vmraid.model.document import Document
from vmraid.utils import add_days


class CropCycle(Document):
	def validate(self):
		self.set_missing_values()

	def after_insert(self):
		self.create_crop_cycle_project()
		self.create_tasks_for_diseases()

	def on_update(self):
		self.create_tasks_for_diseases()

	def set_missing_values(self):
		crop = vmraid.get_doc('Crop', self.crop)

		if not self.crop_spacing_uom:
			self.crop_spacing_uom = crop.crop_spacing_uom

		if not self.row_spacing_uom:
			self.row_spacing_uom = crop.row_spacing_uom

	def create_crop_cycle_project(self):
		crop = vmraid.get_doc('Crop', self.crop)

		self.project = self.create_project(crop.period, crop.agriculture_task)
		self.create_task(crop.agriculture_task, self.project, self.start_date)

	def create_tasks_for_diseases(self):
		for disease in self.detected_disease:
			if not disease.tasks_created:
				self.import_disease_tasks(disease.disease, disease.start_date)
				disease.tasks_created = True

				vmraid.msgprint(_("Tasks have been created for managing the {0} disease (on row {1})").format(disease.disease, disease.idx))

	def import_disease_tasks(self, disease, start_date):
		disease_doc = vmraid.get_doc('Disease', disease)
		self.create_task(disease_doc.treatment_task, self.project, start_date)

	def create_project(self, period, crop_tasks):
		project = vmraid.get_doc({
			"doctype": "Project",
			"project_name": self.title,
			"expected_start_date": self.start_date,
			"expected_end_date": add_days(self.start_date, period - 1)
		}).insert()

		return project.name

	def create_task(self, crop_tasks, project_name, start_date):
		for crop_task in crop_tasks:
			vmraid.get_doc({
				"doctype": "Task",
				"subject": crop_task.get("task_name"),
				"priority": crop_task.get("priority"),
				"project": project_name,
				"exp_start_date": add_days(start_date, crop_task.get("start_day") - 1),
				"exp_end_date": add_days(start_date, crop_task.get("end_day") - 1)
			}).insert()

	@vmraid.whitelist()
	def reload_linked_analysis(self):
		linked_doctypes = ['Soil Texture', 'Soil Analysis', 'Plant Analysis']
		required_fields = ['location', 'name', 'collection_datetime']
		output = {}

		for doctype in linked_doctypes:
			output[doctype] = vmraid.get_all(doctype, fields=required_fields)

		output['Location'] = []

		for location in self.linked_location:
			output['Location'].append(vmraid.get_doc('Location', location.location))

		vmraid.publish_realtime("List of Linked Docs",
								output, user=vmraid.session.user)

	@vmraid.whitelist()
	def append_to_child(self, obj_to_append):
		for doctype in obj_to_append:
			for doc_name in set(obj_to_append[doctype]):
				self.append(doctype, {doctype: doc_name})

		self.save()


def get_coordinates(doc):
	return ast.literal_eval(doc.location).get('features')[0].get('geometry').get('coordinates')


def get_geometry_type(doc):
	return ast.literal_eval(doc.location).get('features')[0].get('geometry').get('type')


def is_in_location(point, vs):
	x, y = point
	inside = False

	j = len(vs) - 1
	i = 0

	while i < len(vs):
		xi, yi = vs[i]
		xj, yj = vs[j]

		intersect = ((yi > y) != (yj > y)) and (
			x < (xj - xi) * (y - yi) / (yj - yi) + xi)

		if intersect:
			inside = not inside

		i = j
		j += 1

	return inside
