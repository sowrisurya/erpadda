from __future__ import unicode_literals
import vmraid
from vmraid.model.utils.rename_field import rename_field

def execute():
	#Rename Grading Structure to Grading Scale
	if not vmraid.db.exists("DocType", "Grading Scale"):
		vmraid.rename_doc("DocType", "Grading Structure", "Grading Scale", force=True)
	if not vmraid.db.exists("DocType", "Grading Scale Interval"):
		vmraid.rename_doc("DocType", "Grade Interval", "Grading Scale Interval", force=True)

	# vmraid.reload_doc("schools", "doctype", "grading_scale_interval")
	vmraid.reload_doc("education", "doctype", "grading_scale_interval")
	if "to_score" in vmraid.db.get_table_columns("Grading Scale Interval"):
		rename_field("Grading Scale Interval", "to_score", "threshold")

	if not vmraid.db.exists("DocType", "Assessment Plan"):
		vmraid.rename_doc("DocType", "Assessment", "Assessment Plan", force=True)

	# 'Schools' module changed to the 'Education'
	# vmraid.reload_doc("schools", "doctype", "assessment_plan")

	#Rename Assessment Results
	vmraid.reload_doc("education", "doctype", "assessment_plan")
	if "grading_structure" in vmraid.db.get_table_columns("Assessment Plan"):
		rename_field("Assessment Plan", "grading_structure", "grading_scale")

	# vmraid.reload_doc("schools", "doctype", "assessment_result")
	# vmraid.reload_doc("schools", "doctype", "assessment_result_detail")
	# vmraid.reload_doc("schools", "doctype", "assessment_criteria")
	vmraid.reload_doc("education", "doctype", "assessment_result")
	vmraid.reload_doc("education", "doctype", "assessment_result_detail")
	vmraid.reload_doc("education", "doctype", "assessment_criteria")


	for assessment in vmraid.get_all("Assessment Plan", 
			fields=["name", "grading_scale"], filters = [["docstatus", "!=", 2 ]]):
		for stud_result in vmraid.db.sql("select * from `tabAssessment Result` where parent= %s", 
				assessment.name, as_dict=True):
			if stud_result.result:
				assessment_result = vmraid.new_doc("Assessment Result")
				assessment_result.student = stud_result.student
				assessment_result.student_name = stud_result.student_name
				assessment_result.assessment_plan = assessment.name
				assessment_result.grading_scale = assessment.grading_scale
				assessment_result.total_score = stud_result.result
				assessment_result.flags.ignore_validate = True
				assessment_result.flags.ignore_mandatory = True
				assessment_result.save()
	
	vmraid.db.sql("""delete from `tabAssessment Result` where parent != '' or parent is not null""")