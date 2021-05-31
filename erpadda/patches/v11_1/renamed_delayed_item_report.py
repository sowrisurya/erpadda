# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
    for report in ["Delayed Order Item Summary", "Delayed Order Summary"]:
        if vmraid.db.exists("Report", report):
            vmraid.delete_doc("Report", report)