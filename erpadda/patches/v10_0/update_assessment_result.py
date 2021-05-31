# Copyright (c) 2017, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc('education', 'doctype', 'assessment_result')

	vmraid.db.sql("""
		UPDATE `tabAssessment Result` AS ar
		INNER JOIN `tabAssessment Plan` AS ap ON ap.name = ar.assessment_plan
		SET ar.academic_term = ap.academic_term,
			ar.academic_year = ap.academic_year,
			ar.program = ap.program,
			ar.course = ap.course,
			ar.assessment_group = ap.assessment_group,
			ar.student_group = ap.student_group
		WHERE ap.docstatus = 1
	""")