import vmraid
from erpadda.portal.product_configurator.utils import (get_products_for_website, get_product_settings,
	get_field_filter_data, get_attribute_filter_data)
from erpadda.shopping_cart.product_query import ProductQuery
from erpadda.shopping_cart.filters import ProductFiltersBuilder

sitemap = 1

def get_context(context):

	if vmraid.form_dict:
		search = vmraid.form_dict.search
		field_filters = vmraid.parse_json(vmraid.form_dict.field_filters)
		attribute_filters = vmraid.parse_json(vmraid.form_dict.attribute_filters)
		start = vmraid.parse_json(vmraid.form_dict.start)
	else:
		search = field_filters = attribute_filters = None
		start = 0

	engine = ProductQuery()
	context.items = engine.query(attribute_filters, field_filters, search, start)

	# Add homepage as parent
	context.parents = [{"name": vmraid._("Home"), "route":"/"}]

	product_settings = get_product_settings()
	filter_engine = ProductFiltersBuilder()

	context.field_filters = filter_engine.get_field_filters()
	context.attribute_filters = filter_engine.get_attribute_fitlers()

	context.product_settings = product_settings
	context.body_class = "product-page"
	context.page_length = product_settings.products_per_page or 20

	context.no_cache = 1
