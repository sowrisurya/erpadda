# -*- coding: utf-8 -*-
# Copyright (c) 2015, ESS LLP and Contributors
# See license.txt
from __future__ import unicode_literals
import unittest
import vmraid
from erpadda.healthcare.doctype.patient_appointment.patient_appointment import update_status, make_encounter
from vmraid.utils import nowdate, add_days, now_datetime
from vmraid.utils.make_random import get_random
from erpadda.accounts.doctype.pos_profile.test_pos_profile import make_pos_profile

class TestPatientAppointment(unittest.TestCase):
	def setUp(self):
		vmraid.db.sql("""delete from `tabPatient Appointment`""")
		vmraid.db.sql("""delete from `tabFee Validity`""")
		vmraid.db.sql("""delete from `tabPatient Encounter`""")
		make_pos_profile()

	def test_status(self):
		patient, medical_department, practitioner = create_healthcare_docs()
		vmraid.db.set_value('Healthcare Settings', None, 'automate_appointment_invoicing', 0)
		appointment = create_appointment(patient, practitioner, nowdate())
		self.assertEqual(appointment.status, 'Open')
		appointment = create_appointment(patient, practitioner, add_days(nowdate(), 2))
		self.assertEqual(appointment.status, 'Scheduled')
		encounter = create_encounter(appointment)
		self.assertEqual(vmraid.db.get_value('Patient Appointment', appointment.name, 'status'), 'Closed')
		encounter.cancel()
		self.assertEqual(vmraid.db.get_value('Patient Appointment', appointment.name, 'status'), 'Open')

	def test_start_encounter(self):
		patient, medical_department, practitioner = create_healthcare_docs()
		vmraid.db.set_value('Healthcare Settings', None, 'automate_appointment_invoicing', 1)
		appointment = create_appointment(patient, practitioner, add_days(nowdate(), 4), invoice = 1)
		appointment.reload()
		self.assertEqual(appointment.invoiced, 1)
		encounter = make_encounter(appointment.name)
		self.assertTrue(encounter)
		self.assertEqual(encounter.company, appointment.company)
		self.assertEqual(encounter.practitioner, appointment.practitioner)
		self.assertEqual(encounter.patient, appointment.patient)
		# invoiced flag mapped from appointment
		self.assertEqual(encounter.invoiced, vmraid.db.get_value('Patient Appointment', appointment.name, 'invoiced'))

	def test_auto_invoicing(self):
		patient, medical_department, practitioner = create_healthcare_docs()
		vmraid.db.set_value('Healthcare Settings', None, 'enable_free_follow_ups', 0)
		vmraid.db.set_value('Healthcare Settings', None, 'automate_appointment_invoicing', 0)
		appointment = create_appointment(patient, practitioner, nowdate())
		self.assertEqual(vmraid.db.get_value('Patient Appointment', appointment.name, 'invoiced'), 0)

		vmraid.db.set_value('Healthcare Settings', None, 'automate_appointment_invoicing', 1)
		appointment = create_appointment(patient, practitioner, add_days(nowdate(), 2), invoice=1)
		self.assertEqual(vmraid.db.get_value('Patient Appointment', appointment.name, 'invoiced'), 1)
		sales_invoice_name = vmraid.db.get_value('Sales Invoice Item', {'reference_dn': appointment.name}, 'parent')
		self.assertTrue(sales_invoice_name)
		self.assertEqual(vmraid.db.get_value('Sales Invoice', sales_invoice_name, 'company'), appointment.company)
		self.assertEqual(vmraid.db.get_value('Sales Invoice', sales_invoice_name, 'patient'), appointment.patient)
		self.assertEqual(vmraid.db.get_value('Sales Invoice', sales_invoice_name, 'paid_amount'), appointment.paid_amount)

	def test_auto_invoicing_based_on_department(self):
		patient, medical_department, practitioner = create_healthcare_docs()
		vmraid.db.set_value('Healthcare Settings', None, 'enable_free_follow_ups', 0)
		vmraid.db.set_value('Healthcare Settings', None, 'automate_appointment_invoicing', 1)
		appointment_type = create_appointment_type()

		appointment = create_appointment(patient, practitioner, add_days(nowdate(), 2),
			invoice=1, appointment_type=appointment_type.name, department='_Test Medical Department')
		appointment.reload()

		self.assertEqual(appointment.invoiced, 1)
		self.assertEqual(appointment.billing_item, 'HLC-SI-001')
		self.assertEqual(appointment.paid_amount, 200)

		sales_invoice_name = vmraid.db.get_value('Sales Invoice Item', {'reference_dn': appointment.name}, 'parent')
		self.assertTrue(sales_invoice_name)
		self.assertEqual(vmraid.db.get_value('Sales Invoice', sales_invoice_name, 'paid_amount'), appointment.paid_amount)

	def test_auto_invoicing_according_to_appointment_type_charge(self):
		patient, medical_department, practitioner = create_healthcare_docs()
		vmraid.db.set_value('Healthcare Settings', None, 'enable_free_follow_ups', 0)
		vmraid.db.set_value('Healthcare Settings', None, 'automate_appointment_invoicing', 1)

		item = create_healthcare_service_items()
		items = [{
				'op_consulting_charge_item': item,
				'op_consulting_charge': 300
		}]
		appointment_type = create_appointment_type(args={
				'name': 'Generic Appointment Type charge',
				'items': items
			})

		appointment = create_appointment(patient, practitioner, add_days(nowdate(), 2),
			invoice=1, appointment_type=appointment_type.name)
		appointment.reload()

		self.assertEqual(appointment.invoiced, 1)
		self.assertEqual(appointment.billing_item, item)
		self.assertEqual(appointment.paid_amount, 300)

		sales_invoice_name = vmraid.db.get_value('Sales Invoice Item', {'reference_dn': appointment.name}, 'parent')
		self.assertTrue(sales_invoice_name)

	def test_appointment_cancel(self):
		patient, medical_department, practitioner = create_healthcare_docs()
		vmraid.db.set_value('Healthcare Settings', None, 'enable_free_follow_ups', 1)
		appointment = create_appointment(patient, practitioner, nowdate())
		fee_validity = vmraid.db.get_value('Fee Validity Reference', {'appointment': appointment.name}, 'parent')
		# fee validity created
		self.assertTrue(fee_validity)

		visited = vmraid.db.get_value('Fee Validity', fee_validity, 'visited')
		update_status(appointment.name, 'Cancelled')
		# check fee validity updated
		self.assertEqual(vmraid.db.get_value('Fee Validity', fee_validity, 'visited'), visited - 1)

		vmraid.db.set_value('Healthcare Settings', None, 'enable_free_follow_ups', 0)
		vmraid.db.set_value('Healthcare Settings', None, 'automate_appointment_invoicing', 1)
		appointment = create_appointment(patient, practitioner, nowdate(), invoice=1)
		update_status(appointment.name, 'Cancelled')
		# check invoice cancelled
		sales_invoice_name = vmraid.db.get_value('Sales Invoice Item', {'reference_dn': appointment.name}, 'parent')
		self.assertEqual(vmraid.db.get_value('Sales Invoice', sales_invoice_name, 'status'), 'Cancelled')

	def test_appointment_booking_for_admission_service_unit(self):
		from erpadda.healthcare.doctype.inpatient_record.inpatient_record import admit_patient, discharge_patient, schedule_discharge
		from erpadda.healthcare.doctype.inpatient_record.test_inpatient_record import \
			create_inpatient, get_healthcare_service_unit, mark_invoiced_inpatient_occupancy

		vmraid.db.sql("""delete from `tabInpatient Record`""")
		patient, medical_department, practitioner = create_healthcare_docs()
		patient = create_patient()
		# Schedule Admission
		ip_record = create_inpatient(patient)
		ip_record.expected_length_of_stay = 0
		ip_record.save(ignore_permissions = True)

		# Admit
		service_unit = get_healthcare_service_unit('Test Service Unit Ip Occupancy')
		admit_patient(ip_record, service_unit, now_datetime())

		appointment = create_appointment(patient, practitioner, nowdate(), service_unit=service_unit)
		self.assertEqual(appointment.service_unit, service_unit)

		# Discharge
		schedule_discharge(vmraid.as_json({'patient': patient}))
		ip_record1 = vmraid.get_doc("Inpatient Record", ip_record.name)
		mark_invoiced_inpatient_occupancy(ip_record1)
		discharge_patient(ip_record1)

	def test_invalid_healthcare_service_unit_validation(self):
		from erpadda.healthcare.doctype.inpatient_record.inpatient_record import admit_patient, discharge_patient, schedule_discharge
		from erpadda.healthcare.doctype.inpatient_record.test_inpatient_record import \
			create_inpatient, get_healthcare_service_unit, mark_invoiced_inpatient_occupancy

		vmraid.db.sql("""delete from `tabInpatient Record`""")
		patient, medical_department, practitioner = create_healthcare_docs()
		patient = create_patient()
		# Schedule Admission
		ip_record = create_inpatient(patient)
		ip_record.expected_length_of_stay = 0
		ip_record.save(ignore_permissions = True)

		# Admit
		service_unit = get_healthcare_service_unit('Test Service Unit Ip Occupancy')
		admit_patient(ip_record, service_unit, now_datetime())

		appointment_service_unit = get_healthcare_service_unit('Test Service Unit Ip Occupancy for Appointment')
		appointment = create_appointment(patient, practitioner, nowdate(), service_unit=appointment_service_unit, save=0)
		self.assertRaises(vmraid.exceptions.ValidationError, appointment.save)

		# Discharge
		schedule_discharge(vmraid.as_json({'patient': patient}))
		ip_record1 = vmraid.get_doc("Inpatient Record", ip_record.name)
		mark_invoiced_inpatient_occupancy(ip_record1)
		discharge_patient(ip_record1)


def create_healthcare_docs():
	patient = create_patient()
	practitioner = vmraid.db.exists('Healthcare Practitioner', '_Test Healthcare Practitioner')
	medical_department = vmraid.db.exists('Medical Department', '_Test Medical Department')

	if not medical_department:
		medical_department = vmraid.new_doc('Medical Department')
		medical_department.department = '_Test Medical Department'
		medical_department.save(ignore_permissions=True)
		medical_department = medical_department.name

	if not practitioner:
		practitioner = vmraid.new_doc('Healthcare Practitioner')
		practitioner.first_name = '_Test Healthcare Practitioner'
		practitioner.gender = 'Female'
		practitioner.department = medical_department
		practitioner.op_consulting_charge = 500
		practitioner.inpatient_visit_charge = 500
		practitioner.save(ignore_permissions=True)
		practitioner = practitioner.name

	return patient, medical_department, practitioner

def create_patient():
	patient = vmraid.db.exists('Patient', '_Test Patient')
	if not patient:
		patient = vmraid.new_doc('Patient')
		patient.first_name = '_Test Patient'
		patient.sex = 'Female'
		patient.save(ignore_permissions=True)
		patient = patient.name
	return patient

def create_encounter(appointment):
	if appointment:
		encounter = vmraid.new_doc('Patient Encounter')
		encounter.appointment = appointment.name
		encounter.patient = appointment.patient
		encounter.practitioner = appointment.practitioner
		encounter.encounter_date = appointment.appointment_date
		encounter.encounter_time = appointment.appointment_time
		encounter.company = appointment.company
		encounter.save()
		encounter.submit()
		return encounter

def create_appointment(patient, practitioner, appointment_date, invoice=0, procedure_template=0,
	service_unit=None, appointment_type=None, save=1, department=None):
	item = create_healthcare_service_items()
	vmraid.db.set_value('Healthcare Settings', None, 'inpatient_visit_charge_item', item)
	vmraid.db.set_value('Healthcare Settings', None, 'op_consulting_charge_item', item)
	appointment = vmraid.new_doc('Patient Appointment')
	appointment.patient = patient
	appointment.practitioner = practitioner
	appointment.department = department or '_Test Medical Department'
	appointment.appointment_date = appointment_date
	appointment.company = '_Test Company'
	appointment.duration = 15
	if service_unit:
		appointment.service_unit = service_unit
	if invoice:
		appointment.mode_of_payment = 'Cash'
	if appointment_type:
		appointment.appointment_type = appointment_type
	if procedure_template:
		appointment.procedure_template = create_clinical_procedure_template().get('name')
	if save:
		appointment.save(ignore_permissions=True)
	return appointment

def create_healthcare_service_items():
	if vmraid.db.exists('Item', 'HLC-SI-001'):
		return 'HLC-SI-001'
	item = vmraid.new_doc('Item')
	item.item_code = 'HLC-SI-001'
	item.item_name = 'Consulting Charges'
	item.item_group = 'Services'
	item.is_stock_item = 0
	item.stock_uom = 'Nos'
	item.save()
	return item.name

def create_clinical_procedure_template():
	if vmraid.db.exists('Clinical Procedure Template', 'Knee Surgery and Rehab'):
		return vmraid.get_doc('Clinical Procedure Template', 'Knee Surgery and Rehab')
	template = vmraid.new_doc('Clinical Procedure Template')
	template.template = 'Knee Surgery and Rehab'
	template.item_code = 'Knee Surgery and Rehab'
	template.item_group = 'Services'
	template.is_billable = 1
	template.description = 'Knee Surgery and Rehab'
	template.rate = 50000
	template.save()
	return template

def create_appointment_type(args=None):
	if not args:
		args =  vmraid.local.form_dict

	name = args.get('name') or 'Test Appointment Type wise Charge'

	if vmraid.db.exists('Appointment Type', name):
		return vmraid.get_doc('Appointment Type', name)

	else:
		item = create_healthcare_service_items()
		items = [{
				'medical_department': '_Test Medical Department',
				'op_consulting_charge_item': item,
				'op_consulting_charge': 200
		}]
		return vmraid.get_doc({
			'doctype': 'Appointment Type',
			'appointment_type': args.get('name') or 'Test Appointment Type wise Charge',
			'default_duration': args.get('default_duration') or 20,
			'color': args.get('color') or '#7575ff',
			'price_list': args.get('price_list') or vmraid.db.get_value("Price List", {"selling": 1}),
			'items': args.get('items') or items
		}).insert()