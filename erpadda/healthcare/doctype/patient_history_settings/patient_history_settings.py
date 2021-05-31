# -*- coding: utf-8 -*-
# Copyright (c) 2020, VMRaid Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import vmraid
import json
from vmraid import _
from vmraid.utils import cstr, cint
from vmraid.model.document import Document
from erpadda.healthcare.page.patient_history.patient_history import get_patient_history_doctypes

class PatientHistorySettings(Document):
	def validate(self):
		self.validate_submittable_doctypes()
		self.validate_date_fieldnames()

	def validate_submittable_doctypes(self):
		for entry in self.custom_doctypes:
			if not cint(vmraid.db.get_value('DocType', entry.document_type, 'is_submittable')):
				msg = _('Row #{0}: Document Type {1} is not submittable. ').format(
					entry.idx, vmraid.bold(entry.document_type))
				msg += _('Patient Medical Record can only be created for submittable document types.')
				vmraid.throw(msg)

	def validate_date_fieldnames(self):
		for entry in self.custom_doctypes:
			field = vmraid.get_meta(entry.document_type).get_field(entry.date_fieldname)
			if not field:
				vmraid.throw(_('Row #{0}: No such Field named {1} found in the Document Type {2}.').format(
					entry.idx, vmraid.bold(entry.date_fieldname), vmraid.bold(entry.document_type)))

			if field.fieldtype not in ['Date', 'Datetime']:
				vmraid.throw(_('Row #{0}: Field {1} in Document Type {2} is not a Date / Datetime field.').format(
					entry.idx, vmraid.bold(entry.date_fieldname), vmraid.bold(entry.document_type)))

	@vmraid.whitelist()
	def get_doctype_fields(self, document_type, fields):
		multicheck_fields = []
		doc_fields = vmraid.get_meta(document_type).fields

		for field in doc_fields:
			if field.fieldtype not in vmraid.model.no_value_fields or \
				field.fieldtype in vmraid.model.table_fields and not field.hidden:
				multicheck_fields.append({
					'label': field.label,
					'value': field.fieldname,
					'checked': 1 if field.fieldname in fields else 0
				})

		return multicheck_fields

	@vmraid.whitelist()
	def get_date_field_for_dt(self, document_type):
		meta = vmraid.get_meta(document_type)
		date_fields = meta.get('fields', {
			'fieldtype': ['in', ['Date', 'Datetime']]
		})

		if date_fields:
			return date_fields[0].get('fieldname')

def create_medical_record(doc, method=None):
	medical_record_required = validate_medical_record_required(doc)
	if not medical_record_required:
		return

	if vmraid.db.exists('Patient Medical Record', { 'reference_name': doc.name }):
		return

	subject = set_subject_field(doc)
	date_field = get_date_field(doc.doctype)
	medical_record = vmraid.new_doc('Patient Medical Record')
	medical_record.patient = doc.patient
	medical_record.subject = subject
	medical_record.status = 'Open'
	medical_record.communication_date = doc.get(date_field)
	medical_record.reference_doctype = doc.doctype
	medical_record.reference_name = doc.name
	medical_record.reference_owner = doc.owner
	medical_record.save(ignore_permissions=True)


def update_medical_record(doc, method=None):
	medical_record_required = validate_medical_record_required(doc)
	if not medical_record_required:
		return

	medical_record_id = vmraid.db.exists('Patient Medical Record', { 'reference_name': doc.name })

	if medical_record_id:
		subject = set_subject_field(doc)
		vmraid.db.set_value('Patient Medical Record', medical_record_id[0][0], 'subject', subject)
	else:
		create_medical_record(doc)


def delete_medical_record(doc, method=None):
	medical_record_required = validate_medical_record_required(doc)
	if not medical_record_required:
		return

	record = vmraid.db.exists('Patient Medical Record', { 'reference_name': doc.name })
	if record:
		vmraid.delete_doc('Patient Medical Record', record, force=1)


def set_subject_field(doc):
	from vmraid.utils.formatters import format_value

	meta = vmraid.get_meta(doc.doctype)
	subject = ''
	patient_history_fields = get_patient_history_fields(doc)

	for entry in patient_history_fields:
		fieldname = entry.get('fieldname')
		if entry.get('fieldtype') == 'Table' and doc.get(fieldname):
			formatted_value = get_formatted_value_for_table_field(doc.get(fieldname), meta.get_field(fieldname))
			subject += vmraid.bold(_(entry.get('label')) + ': ') + '<br>' + cstr(formatted_value) + '<br>'

		else:
			if doc.get(fieldname):
				formatted_value = format_value(doc.get(fieldname), meta.get_field(fieldname), doc)
				subject += vmraid.bold(_(entry.get('label')) + ': ') + cstr(formatted_value) + '<br>'

	return subject


def get_date_field(doctype):
	dt = get_patient_history_config_dt(doctype)

	return vmraid.db.get_value(dt, { 'document_type': doctype }, 'date_fieldname')


def get_patient_history_fields(doc):
	dt = get_patient_history_config_dt(doc.doctype)
	patient_history_fields = vmraid.db.get_value(dt, { 'document_type': doc.doctype }, 'selected_fields')

	if patient_history_fields:
		return json.loads(patient_history_fields)


def get_formatted_value_for_table_field(items, df):
	child_meta = vmraid.get_meta(df.options)

	table_head = ''
	table_row = ''
	html = ''
	create_head = True
	for item in items:
		table_row += '<tr>'
		for cdf in child_meta.fields:
			if cdf.in_list_view:
				if create_head:
					table_head += '<td>' + cdf.label + '</td>'
				if item.get(cdf.fieldname):
					table_row += '<td>' + str(item.get(cdf.fieldname)) + '</td>'
				else:
					table_row += '<td></td>'
		create_head = False
		table_row += '</tr>'

	html += "<table class='table table-condensed table-bordered'>" + table_head +  table_row + "</table>"

	return html


def get_patient_history_config_dt(doctype):
	if vmraid.db.get_value('DocType', doctype, 'custom'):
		return 'Patient History Custom Document Type'
	else:
		return 'Patient History Standard Document Type'


def validate_medical_record_required(doc):
	if vmraid.flags.in_patch or vmraid.flags.in_install or vmraid.flags.in_setup_wizard \
		or get_module(doc) != 'Healthcare':
		return False

	if doc.doctype not in get_patient_history_doctypes():
		return False

	return True

def get_module(doc):
	module = doc.meta.module
	if not module:
		module = vmraid.db.get_value('DocType', doc.doctype, 'module')

	return module