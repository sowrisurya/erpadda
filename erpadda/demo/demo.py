from __future__ import unicode_literals

import vmraid, sys
import erpadda
import vmraid.utils
from erpadda.demo.user import hr, sales, purchase, manufacturing, stock, accounts, projects, fixed_asset
from erpadda.demo.user import education as edu
from erpadda.demo.setup import education, manufacture, setup_data, healthcare, retail
"""
Make a demo

1. Start with a fresh account

bench --site demo.erpadda.dev reinstall

2. Install Demo

bench --site demo.erpadda.dev execute erpadda.demo.demo.make

3. If Demo breaks, to continue

bench --site demo.erpadda.dev execute erpadda.demo.demo.simulate

"""

def make(domain='Manufacturing', days=100):
	vmraid.flags.domain = domain
	vmraid.flags.mute_emails = True
	setup_data.setup(domain)
	if domain== 'Manufacturing':
		manufacture.setup_data()
	elif domain == "Retail":
		retail.setup_data()
	elif domain== 'Education':
		education.setup_data()
	elif domain== 'Healthcare':
		healthcare.setup_data()

	site = vmraid.local.site
	vmraid.destroy()
	vmraid.init(site)
	vmraid.connect()

	simulate(domain, days)

def simulate(domain='Manufacturing', days=100):
	runs_for = vmraid.flags.runs_for or days
	vmraid.flags.company = erpadda.get_default_company()
	vmraid.flags.mute_emails = True

	if not vmraid.flags.start_date:
		# start date = 100 days back
		vmraid.flags.start_date = vmraid.utils.add_days(vmraid.utils.nowdate(),
			-1 * runs_for)

	current_date = vmraid.utils.getdate(vmraid.flags.start_date)

	# continue?
	demo_last_date = vmraid.db.get_global('demo_last_date')
	if demo_last_date:
		current_date = vmraid.utils.add_days(vmraid.utils.getdate(demo_last_date), 1)

	# run till today
	if not runs_for:
		runs_for = vmraid.utils.date_diff(vmraid.utils.nowdate(), current_date)
		# runs_for = 100

	fixed_asset.work()
	for i in range(runs_for):
		sys.stdout.write("\rSimulating {0}: Day {1}".format(
			current_date.strftime("%Y-%m-%d"), i))
		sys.stdout.flush()
		vmraid.flags.current_date = current_date
		if current_date.weekday() in (5, 6):
			current_date = vmraid.utils.add_days(current_date, 1)
			continue
		try:
			hr.work()
			purchase.work()
			stock.work()
			accounts.work()
			projects.run_projects(current_date)
			sales.work(domain)
			# run_messages()

			if domain=='Manufacturing':
				manufacturing.work()
			elif domain=='Education':
				edu.work()

		except:
			vmraid.db.set_global('demo_last_date', current_date)
			raise
		finally:
			current_date = vmraid.utils.add_days(current_date, 1)
			vmraid.db.commit()
