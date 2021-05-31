from __future__ import unicode_literals
import vmraid

from erpadda.setup.install import create_print_zero_amount_taxes_custom_field

def execute():
	vmraid.reload_doc('printing', 'doctype', 'print_style')
	vmraid.reload_doc('printing', 'doctype', 'print_settings')
	create_print_zero_amount_taxes_custom_field()