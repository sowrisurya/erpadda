# Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid
from vmraid.model.utils.rename_field import rename_field

def execute():
    vmraid.reload_doc('projects', 'doctype', 'project')

    if vmraid.db.has_column('Project', 'from'):
        rename_field('Project', 'from', 'from_time')
        rename_field('Project', 'to', 'to_time')