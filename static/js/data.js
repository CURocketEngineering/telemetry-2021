var refresh_period = 500;  // 500 ms
var socket; 

function request_data() {
	console.log("data requested");
	socket.emit("request_data");
	setTimeout(request_data, refresh_period);
}

function receive_data(data) {
	console.log("data received", data);
	add_data_to_charts(data);
	$("#testing").text($("#testing").text()+"?");
}

function show_settings_modal() {
	$("#settings_modal").modal(
		{
			show: true,
			focus: true,
			keyboard: true,
		}
	);
}

function hide_settings_modal() {
	$("#settings_modal").modal(
		{
			show: false,
			keyboard: true,
		}
	);
}

var data_type = "live"
function set_data_type(t) {
	data_type = t;
}

function set_data_mode() {
	var filename = $("#data_file").val();
	console.log(data_type, filename);
}

$(document).ready(() => {
	socket = io();
	socket.on("connect", () => {
		console.log("Socketio connected.");
		show_settings_modal();
		//socket.on("receive_data", receive_data);
		//setTimeout(request_data, refresh_period);
	});
})
