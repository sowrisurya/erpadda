# Copyright (c) 2020, VMRaid Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
    vmraid.reload_doc("hr", "doctype", "employee")

    if vmraid.db.has_column("Employee", "reason_for_resignation"):
        vmraid.db.sql(""" UPDATE `tabEmployee`
            SET reason_for_leaving = reason_for_resignation
            WHERE status = 'Left' and reason_for_leaving is null and reason_for_resignation is not null
        """)

