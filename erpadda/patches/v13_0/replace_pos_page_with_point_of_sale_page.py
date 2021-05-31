from __future__ import unicode_literals
import vmraid

def execute():
	if vmraid.db.exists("Page", "point-of-sale"):
		vmraid.rename_doc("Page", "pos", "point-of-sale", 1, 1)