from __future__ import unicode_literals
import vmraid
from erpadda.regional.india.setup import setup

def execute():
	company = vmraid.get_all('Company', filters = {'country': 'India'})
	if not company:
		return

	# call setup for india
	setup(patch=True)