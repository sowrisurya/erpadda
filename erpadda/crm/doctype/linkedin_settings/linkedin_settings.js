// Copyright (c) 2020, VMRaid Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

vmraid.ui.form.on('LinkedIn Settings', {
	onload: function(frm){
		if (frm.doc.session_status == 'Expired' && frm.doc.consumer_key && frm.doc.consumer_secret){
			vmraid.confirm(
				__('Session not valid, Do you want to login?'),
				function(){
					frm.trigger("login");
				},
				function(){
					window.close();
				}
			);
		}
	},
	refresh: function(frm){
		if (frm.doc.session_status=="Expired"){
			let msg = __("Session Not Active. Save doc to login.");
			frm.dashboard.set_headline_alert(
				`<div class="row">
					<div class="col-xs-12">
						<span class="indicator whitespace-nowrap red"><span class="hidden-xs">${msg}</span></span>
					</div>
				</div>`
			);
		}

		if (frm.doc.session_status=="Active"){
			let d = new Date(frm.doc.modified);
			d.setDate(d.getDate()+60);
			let dn = new Date();
			let days = d.getTime() - dn.getTime();
			days = Math.floor(days/(1000 * 3600 * 24));
			let msg,color;

			if (days>0){
				msg = __("Your Session will be expire in ") + days + __(" days.");
				color = "green";
			}
			else {
				msg = __("Session is expired. Save doc to login.");
				color = "red";
			}

			frm.dashboard.set_headline_alert(
				`<div class="row">
					<div class="col-xs-12">
						<span class="indicator whitespace-nowrap ${color}"><span class="hidden-xs">${msg}</span></span>
					</div>
				</div>`
			);
		}
	},
	login: function(frm){
		if (frm.doc.consumer_key && frm.doc.consumer_secret){
			vmraid.dom.freeze();
			vmraid.call({
				doc: frm.doc,
				method: "get_authorization_url",
				callback : function(r) {
					window.location.href = r.message;
				}
			}).fail(function() {
				vmraid.dom.unfreeze();
			});
		}
	},
	after_save: function(frm){
		frm.trigger("login");
	}
});
