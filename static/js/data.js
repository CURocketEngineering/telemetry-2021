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

function show_telemetry_actions_modal() {
	$("#telemetry_actions_modal").modal(
		{
			show: true,
			focus: true,
			keyboard: true,
		}
	);
}

function hide_telemetry_actions_modal() {
	$("#telemetry_actions_modal").modal(
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

function start_requesting_data() {
	clear_charts();
	socket.on("receive_data", receive_data);
	setTimeout(request_data, refresh_period);
}

function halt() {
	socket.emit("halt");
}

function arm() {
	socket.emit("arm");
}

function eject1() {
	socket.emit("eject1");
}

function eject2() {
	socket.emit("eject2");
}

function resume() {
	socket.emit("resume");
}

function demo_simulation() {
	socket.emit("demo_simulation");
}

$(document).ready(() => {
	socket = io();
	socket.on("connect", () => {
		console.log("Socketio connected.");
		show_settings_modal();
	});
})
