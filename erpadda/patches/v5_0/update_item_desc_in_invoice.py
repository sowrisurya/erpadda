# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.website.utils import find_first_image
from vmraid.utils import cstr
import re

def execute():
	item_details = vmraid._dict()
	for d in vmraid.db.sql("select name, description, image from `tabItem`", as_dict=1):
		description = cstr(d.description).strip()
		item_details.setdefault(d.name, vmraid._dict({
			"description": description,
			"image": d.image
		}))


	dt_list= ["Sales Invoice Item","Purchase Invoice Item"]
	for dt in dt_list:
		vmraid.reload_doctype(dt)
		records = vmraid.db.sql("""select name, item_code, description from `tab{0}`
			where ifnull(item_code, '') != '' and description is not null """.format(dt), as_dict=1)

		count = 1
		for d in records:
			if item_details.get(d.item_code) and cstr(d.description) == item_details.get(d.item_code).description:
				desc = item_details.get(d.item_code).description
				image = item_details.get(d.item_code).image
			else:
				desc, image = extract_image_and_description(cstr(d.description))

				if not image:
					item_detail = item_details.get(d.item_code)
					if item_detail:
						image = item_detail.image

			vmraid.db.sql("""update `tab{0}` set description = %s, image = %s
				where name = %s """.format(dt), (desc, image, d.name))

			count += 1
			if count % 500 == 0:
				vmraid.db.commit()


def extract_image_and_description(data):
	image_url = find_first_image(data)
	desc = data
	for tag in ("img", "table", "tr", "td"):
		desc =  re.sub("\</*{0}[^>]*\>".format(tag), "", desc)
	return desc, image_url