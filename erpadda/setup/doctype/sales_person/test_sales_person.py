# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
from __future__ import unicode_literals

test_dependencies = ["Employee"]

import vmraid
test_records = vmraid.get_test_records('Sales Person')

test_ignore = ["Item Group"]
