// Copyright (c) 2015, VMRaid Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt



vmraid.provide("erpadda.hr");

erpadda.hr.AttendanceControlPanel = class AttendanceControlPanel extends vmraid.ui.form.Controller {
	onload() {
		this.frm.set_value("att_fr_date", vmraid.datetime.get_today());
		this.frm.set_value("att_to_date", vmraid.datetime.get_today());
	}

	refresh() {
		this.frm.disable_save();
		this.show_upload();
		this.setup_import_progress();
	}

	get_template() {
		if(!this.frm.doc.att_fr_date || !this.frm.doc.att_to_date) {
			vmraid.msgprint(__("Attendance From Date and Attendance To Date is mandatory"));
			return;
		}
		window.location.href = repl(vmraid.request.url +
			'?cmd=%(cmd)s&from_date=%(from_date)s&to_date=%(to_date)s', {
			cmd: "erpadda.hr.doctype.upload_attendance.upload_attendance.get_template",
			from_date: this.frm.doc.att_fr_date,
			to_date: this.frm.doc.att_to_date,
		});
	}

	show_upload() {
		var $wrapper = $(cur_frm.fields_dict.upload_html.wrapper).empty();
		new vmraid.ui.FileUploader({
			wrapper: $wrapper,
			method: 'erpadda.hr.doctype.upload_attendance.upload_attendance.upload'
		});
	}

	setup_import_progress() {
		var $log_wrapper = $(this.frm.fields_dict.import_log.wrapper).empty();

		vmraid.realtime.on('import_attendance', (data) => {
			if (data.progress) {
				this.frm.dashboard.show_progress('Import Attendance', data.progress / data.total * 100,
					__('Importing {0} of {1}', [data.progress, data.total]));
				if (data.progress === data.total) {
					this.frm.dashboard.hide_progress('Import Attendance');
				}
			} else if (data.error) {
				this.frm.dashboard.hide();
				let messages = [`<th>${__('Error in some rows')}</th>`].concat(data.messages
					.filter(message => message.includes('Error'))
					.map(message => `<tr><td>${message}</td></tr>`))
					.join('');
				$log_wrapper.append('<table class="table table-bordered">' + messages);
			} else if (data.messages) {
				this.frm.dashboard.hide();
				let messages = [`<th>${__('Import Successful')}</th>`].concat(data.messages
					.map(message => `<tr><td>${message}</td></tr>`))
					.join('');
				$log_wrapper.append('<table class="table table-bordered">' + messages);
			}
		});
	}
}

cur_frm.cscript = new erpadda.hr.AttendanceControlPanel({frm: cur_frm});