import vmraid
from vmraid import _
from vmraid.contacts.doctype.address.address import Address
from vmraid.contacts.doctype.address.address import get_address_templates

class ERPAddaAddress(Address):
	def validate(self):
		self.validate_reference()
		super(ERPAddaAddress, self).validate()

	def link_address(self):
		"""Link address based on owner"""
		if self.is_your_company_address:
			return

		return super(ERPAddaAddress, self).link_address()

	def validate_reference(self):
		if self.is_your_company_address and not [
			row for row in self.links if row.link_doctype == "Company"
		]:
			vmraid.throw(_("Address needs to be linked to a Company. Please add a row for Company in the Links table."),
				title=_("Company Not Linked"))

@vmraid.whitelist()
def get_shipping_address(company, address = None):
	filters = [
		["Dynamic Link", "link_doctype", "=", "Company"],
		["Dynamic Link", "link_name", "=", company],
		["Address", "is_your_company_address", "=", 1]
	]
	fields = ["*"]
	if address and vmraid.db.get_value('Dynamic Link',
		{'parent': address, 'link_name': company}):
		filters.append(["Address", "name", "=", address])

	address = vmraid.get_all("Address", filters=filters, fields=fields) or {}

	if address:
		address_as_dict = address[0]
		name, address_template = get_address_templates(address_as_dict)
		return address_as_dict.get("name"), vmraid.render_template(address_template, address_as_dict)
