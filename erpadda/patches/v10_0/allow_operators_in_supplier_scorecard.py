# Copyright (c) 2019, VMRaid and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import vmraid

def execute():
	vmraid.reload_doc('buying', 'doctype', 'supplier_scorecard_criteria')
	vmraid.reload_doc('buying', 'doctype', 'supplier_scorecard_scoring_criteria')
	vmraid.reload_doc('buying', 'doctype', 'supplier_scorecard')

	for criteria in vmraid.get_all('Supplier Scorecard Criteria', fields=['name', 'formula'], limit_page_length=None):
		vmraid.db.set_value('Supplier Scorecard Criteria', criteria.name,
			'formula', criteria.formula.replace('&lt;','<').replace('&gt;','>'))

	for criteria in vmraid.get_all('Supplier Scorecard Scoring Criteria', fields=['name', 'formula'], limit_page_length=None):
		if criteria.formula: # not mandatory
			vmraid.db.set_value('Supplier Scorecard Scoring Criteria', criteria.name,
				'formula', criteria.formula.replace('&lt;','<').replace('&gt;','>'))

	for sc in vmraid.get_all('Supplier Scorecard', fields=['name', 'weighting_function'], limit_page_length=None):
		vmraid.db.set_value('Supplier Scorecard', sc.name, 'weighting_function',
			sc.weighting_function.replace('&lt;','<').replace('&gt;','>'))