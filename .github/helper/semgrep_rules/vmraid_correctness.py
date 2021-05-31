import vmraid
from vmraid import _, flt

from vmraid.model.document import Document


def on_submit(self):
	if self.value_of_goods == 0:
		vmraid.throw(_('Value of goods cannot be 0'))
	# ruleid: vmraid-modifying-after-submit
	self.status = 'Submitted'

def on_submit(self):
	if flt(self.per_billed) < 100:
		self.update_billing_status()
	else:
		# todook: vmraid-modifying-after-submit
		self.status = "Completed"
		self.db_set("status", "Completed")

class TestDoc(Document):
	pass

	def validate(self):
		#ruleid: vmraid-modifying-child-tables-while-iterating
		for item in self.child_table:
			if item.value < 0:
				self.remove(item)
