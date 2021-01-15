var gyro_config = {
    type: 'line',
    data: {
        datasets: [
            {
                label: 'X',
                borderColor: 'rgba(255,0,0,0.8)',
                backgroundColor: 'rgba(255,0,0,0.8)',
                fill: false,
				pointRadius: 0,
            },
            {
                label: 'Y',
                borderColor: 'rgba(0,255,0,0.8)',
                backgroundColor: 'rgba(0,255,0,0.8)',
                fill: false,
				pointRadius: 0,
            },
            {
                label: 'Z',
                borderColor: 'rgba(0,0,255,0.8)',
                backgroundColor: 'rgba(0,0,255,0.8)',
                fill: false,
				pointRadius: 0,
            },
        ]
    },
    options: {
        responsive: true,
        title:{
            display: true,
            text: 'Gyroscopes'
        },
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Timestamp'
                }
            }],
            yAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Gyro-value'
                }
            }]
        }
    }
};
var alt_config = {
    type: 'line',
    data: {
        datasets: [
            {
                label: 'Altitude',
                borderColor: 'rgba(255,0,0,0.8)',
                backgroundColor: 'rgba(255,0,0,0.8)',
                fill: false,
				pointRadius: 0,
            }
        ]
    },
    options: {
        responsive: true,
        title:{
            display: true,
            text: 'Altitude'
        },
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Timestamp'
                }
            }],
            yAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Altitude'
                }
            }]
        }
    }
};

function add_data_to_charts(data) {
	if (Object.keys(data).length === 0) {
		console.log("No data yet");
		return;
	}
	for (let i = 0; i < data.time.length; i++) {
		// Gyroscope
		gyro_config.data.labels.push(data.time[i]);
		gyro_config.data.datasets[0].data.push(data.sensors.gyro.x[i]);
		gyro_config.data.datasets[1].data.push(data.sensors.gyro.y[i]);
		gyro_config.data.datasets[2].data.push(data.sensors.gyro.z[i]);

		// Altitude
		alt_config.data.labels.push(data.time[i]);
		alt_config.data.datasets[0].data.push(data.sensors.alt[i]);
	}
	if (data.time.length > 0){
		console.log(charts);
		charts.forEach( (chart) => {
			console.log(chart);
			chart.update();
		});
	}
}

function clear_charts() {
	configs.forEach( (config) => {
		config.data.labels = [];
		config.data.datasets.forEach( (dataset) => {
			dataset.data = [];
		});
	});
}


var charts = [];
var configs = [];
$(document).ready(() => {
	var alt_ctx = $("#alt_canvas")[0].getContext('2d');
	var alt_chart = new Chart(alt_ctx, alt_config);
	var gyro_ctx = $("#gyro_canvas")[0].getContext('2d');
    var gyro_chart = new Chart(gyro_ctx, gyro_config);

	configs.push(alt_chart, gyro_chart);
	charts.push(alt_chart, gyro_chart);
})
