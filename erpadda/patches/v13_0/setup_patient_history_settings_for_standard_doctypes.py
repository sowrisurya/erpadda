from __future__ import unicode_literals
import vmraid
from erpadda.healthcare.setup import setup_patient_history_settings

def execute():
	if "Healthcare" not in vmraid.get_active_domains():
		return

	vmraid.reload_doc("healthcare", "doctype", "Inpatient Medication Order")
	vmraid.reload_doc("healthcare", "doctype", "Therapy Session")
	vmraid.reload_doc("healthcare", "doctype", "Clinical Procedure")
	vmraid.reload_doc("healthcare", "doctype", "Patient History Settings")
	vmraid.reload_doc("healthcare", "doctype", "Patient History Standard Document Type")
	vmraid.reload_doc("healthcare", "doctype", "Patient History Custom Document Type")

	setup_patient_history_settings()