vmraid.provide('hub');
vmraid.provide('erpadda.hub');

erpadda.hub.cache = {};
hub.call = function call_hub_method(method, args={}, clear_cache_on_event) { // eslint-disable-line
	return new Promise((resolve, reject) => {

		// cache
		const key = method + JSON.stringify(args);
		if (erpadda.hub.cache[key]) {
			resolve(erpadda.hub.cache[key]);
		}

		// cache invalidation
		const clear_cache = () => delete erpadda.hub.cache[key];

		if (!clear_cache_on_event) {
			invalidate_after_5_mins(clear_cache);
		} else {
			erpadda.hub.on(clear_cache_on_event, () => {
				clear_cache(key);
			});
		}

		let res;
		if (hub.is_server) {
			res = vmraid.call({
				method: 'hub.hub.api.' + method,
				args
			});
		} else {
			res = vmraid.call({
				method: 'erpadda.hub_node.api.call_hub_method',
				args: {
					method,
					params: args
				}
			});
		}

		res.then(r => {
			if (r.message) {
				const response = r.message;
				if (response.error) {
					vmraid.throw({
						title: __('Marketplace Error'),
						message: response.error
					});
				}

				erpadda.hub.cache[key] = response;
				erpadda.hub.trigger(`response:${key}`, { response });
				resolve(response);
			}
			reject(r);

		}).fail(reject);
	});
};

function invalidate_after_5_mins(clear_cache) {
	// cache invalidation after 5 minutes
	const timeout = 5 * 60 * 1000;

	setTimeout(() => {
		clear_cache();
	}, timeout);
}
