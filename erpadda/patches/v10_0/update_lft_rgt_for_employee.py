from __future__ import unicode_literals
import vmraid
from vmraid.utils.nestedset import rebuild_tree

def execute():
    """ assign lft and rgt appropriately """
    vmraid.reload_doc("hr", "doctype", "employee")

    rebuild_tree("Employee", "reports_to")