var refresh_period = 500;  // 500 ms
var socket; 

function request_data() {
	console.log("data requested");
	socket.emit("request_data");
	setTimeout(request_data, refresh_period);
}

function receive_data(data) {
	console.log("data received", data);
	$("#testing").text($("#testing").text()+"?");
}

$(document).ready(() => {
	console.log("Graphing ready.");
	socket = io();
	socket.on("connect", () => {
		console.log("Socketio connected.");
		socket.on("receive_data", receive_data);
		setTimeout(request_data, refresh_period);
	});
})
