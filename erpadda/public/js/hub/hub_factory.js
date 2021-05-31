vmraid.provide('erpadda.hub');

vmraid.views.MarketplaceFactory = class MarketplaceFactory extends vmraid.views.Factory {
	show() {
		is_marketplace_disabled()
			.then(disabled => {
				if (disabled) {
					vmraid.show_not_found('Marketplace');
					return;
				}

				if (vmraid.pages.marketplace) {
					vmraid.container.change_to('marketplace');
					erpadda.hub.marketplace.refresh();
				} else {
					this.make('marketplace');
				}
			});
	}

	make(page_name) {
		vmraid.require('marketplace.bundle.js', () => {
			erpadda.hub.marketplace = new erpadda.hub.Marketplace({
				parent: this.make_page(true, page_name)
			});
		});
	}
};

function is_marketplace_disabled() {
	return vmraid.call({
		method: "erpadda.hub_node.doctype.marketplace_settings.marketplace_settings.is_marketplace_enabled"
	}).then(r => r.message)
}
