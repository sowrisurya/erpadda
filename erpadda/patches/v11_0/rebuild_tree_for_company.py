from __future__ import unicode_literals
import vmraid
from vmraid.utils.nestedset import rebuild_tree

def execute():
	vmraid.reload_doc("setup", "doctype", "company")
	rebuild_tree('Company', 'parent_company')
