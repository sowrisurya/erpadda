from __future__ import unicode_literals
import vmraid
import erpadda

def execute():
	vmraid.reload_doc('portal', 'doctype', 'homepage_featured_product')
	vmraid.reload_doc('portal', 'doctype', 'homepage')
	vmraid.reload_doc('portal', 'doctype', 'products_settings')
	vmraid.reload_doctype('Item')
	vmraid.reload_doctype('Item Group')

	website_settings = vmraid.get_doc('Website Settings', 'Website Settings')
	if vmraid.db.exists('Web Page', website_settings.home_page):
		header = vmraid.db.get_value('Web Page', website_settings.home_page, 'header')
		if header and header.startswith("<div class='hero text-center'>"):
			homepage = vmraid.get_doc('Homepage', 'Homepage')
			homepage.company = erpadda.get_default_company() or vmraid.get_all("Company")[0].name
			if '<h1>' in header:
				homepage.tag_line = header.split('<h1>')[1].split('</h1>')[0] or 'Default Website'
			else:
				homepage.tag_line = 'Default Website'
			homepage.setup_items()
			homepage.save()

			website_settings.home_page = 'home'
			website_settings.save()

