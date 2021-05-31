from __future__ import unicode_literals
import json, os

from vmraid.desk.page.setup_wizard.setup_wizard import setup_complete
from erpadda.setup.setup_wizard import setup_wizard

def complete():
	with open(os.path.join(os.path.dirname(__file__),
		'data', 'test_mfg.json'), 'r') as f:
		data = json.loads(f.read())

	setup_complete(data)
