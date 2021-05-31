# Copyright (c) 2019, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import vmraid

def execute():
    vmraid.reload_doc("stock", "doctype", "pick_list")
    vmraid.db.sql("""UPDATE `tabPick List` set purpose = 'Delivery'
        WHERE docstatus = 1  and purpose = 'Delivery against Sales Order' """)