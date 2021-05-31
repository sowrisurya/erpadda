vmraid.provide('vmraid.dashboards.chart_sources');

vmraid.dashboards.chart_sources["Department wise Patient Appointments"] = {
	method: "erpadda.healthcare.dashboard_chart_source.department_wise_patient_appointments.department_wise_patient_appointments.get",
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: vmraid.defaults.get_user_default("Company")
		}
	]
};