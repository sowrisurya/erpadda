# -*- coding: utf-8 -*-
# Copyright (c) 2015, ESS LLP and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
from vmraid import _
from vmraid.model.document import Document
from vmraid.utils import cstr, getdate, add_days
from vmraid import _
from vmraid.model.mapper import get_mapped_doc

class PatientEncounter(Document):
	def validate(self):
		self.set_title()

	def on_update(self):
		if self.appointment:
			vmraid.db.set_value('Patient Appointment', self.appointment, 'status', 'Closed')

	def on_submit(self):
		if self.therapies:
			create_therapy_plan(self)

	def on_cancel(self):
		if self.appointment:
			vmraid.db.set_value('Patient Appointment', self.appointment, 'status', 'Open')

		if self.inpatient_record and self.drug_prescription:
			delete_ip_medication_order(self)

	def set_title(self):
		self.title = _('{0} with {1}').format(self.patient_name or self.patient,
			self.practitioner_name or self.practitioner)[:100]

@vmraid.whitelist()
def make_ip_medication_order(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.start_date = source.encounter_date
		for entry in source.drug_prescription:
			if entry.drug_code:
				dosage = vmraid.get_doc('Prescription Dosage', entry.dosage)
				dates = get_prescription_dates(entry.period, target.start_date)
				for date in dates:
					for dose in dosage.dosage_strength:
						order = target.append('medication_orders')
						order.drug = entry.drug_code
						order.drug_name = entry.drug_name
						order.dosage = dose.strength
						order.instructions = entry.comment
						order.dosage_form = entry.dosage_form
						order.date = date
						order.time = dose.strength_time
				target.end_date = dates[-1]

	doc = get_mapped_doc('Patient Encounter', source_name, {
			'Patient Encounter': {
				'doctype': 'Inpatient Medication Order',
				'field_map': {
					'name': 'patient_encounter',
					'patient': 'patient',
					'patient_name': 'patient_name',
					'patient_age': 'patient_age',
					'inpatient_record': 'inpatient_record',
					'practitioner': 'practitioner',
					'start_date': 'encounter_date'
				},
			}
		}, target_doc, set_missing_values)

	return doc


def get_prescription_dates(period, start_date):
	prescription_duration = vmraid.get_doc('Prescription Duration', period)
	days = prescription_duration.get_days()
	dates = [start_date]
	for i in range(1, days):
		dates.append(add_days(getdate(start_date), i))
	return dates


def create_therapy_plan(encounter):
	if len(encounter.therapies):
		doc = vmraid.new_doc('Therapy Plan')
		doc.patient = encounter.patient
		doc.start_date = encounter.encounter_date
		for entry in encounter.therapies:
			doc.append('therapy_plan_details', {
				'therapy_type': entry.therapy_type,
				'no_of_sessions': entry.no_of_sessions
			})
		doc.save(ignore_permissions=True)
		if doc.get('name'):
			encounter.db_set('therapy_plan', doc.name)
			vmraid.msgprint(_('Therapy Plan {0} created successfully.').format(vmraid.bold(doc.name)), alert=True)


def delete_ip_medication_order(encounter):
	record = vmraid.db.exists('Inpatient Medication Order', {'patient_encounter': encounter.name})
	if record:
		vmraid.delete_doc('Inpatient Medication Order', record, force=1)