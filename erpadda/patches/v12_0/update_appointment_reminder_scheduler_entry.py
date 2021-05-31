import vmraid

def execute():
	job = vmraid.db.exists('Scheduled Job Type', 'patient_appointment.send_appointment_reminder')
	if job:
		method = 'erpadda.healthcare.doctype.patient_appointment.patient_appointment.send_appointment_reminder'
		vmraid.db.set_value('Scheduled Job Type', job, 'method', method)