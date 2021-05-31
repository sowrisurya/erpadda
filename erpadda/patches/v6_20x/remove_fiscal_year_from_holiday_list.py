from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doctype("Holiday List")

	default_holiday_list = vmraid.db.get_value("Holiday List", {"is_default": 1})
	if default_holiday_list:
		for company in vmraid.get_all("Company", fields=["name", "default_holiday_list"]):
			if not company.default_holiday_list:
				vmraid.db.set_value("Company", company.name, "default_holiday_list", default_holiday_list)


	fiscal_years = vmraid._dict((fy.name, fy) for fy in vmraid.get_all("Fiscal Year", fields=["name", "year_start_date", "year_end_date"]))

	for holiday_list in vmraid.get_all("Holiday List", fields=["name", "fiscal_year"]):
		fy = fiscal_years[holiday_list.fiscal_year]
		vmraid.db.set_value("Holiday List", holiday_list.name, "from_date", fy.year_start_date)
		vmraid.db.set_value("Holiday List", holiday_list.name, "to_date", fy.year_end_date)
