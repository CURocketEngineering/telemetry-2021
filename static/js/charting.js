var chart_config = {
    type: 'line',
    data: {
        datasets: [
            {
                label: 'X',
                borderColor: 'rgba(255,0,0,0.8)',
                backgroundColor: 'rgba(255,0,0,0.8)',
                fill: false,
            },
            {
                label: 'Y',
                borderColor: 'rgba(0,255,0,0.8)',
                backgroundColor: 'rgba(0,255,0,0.8)',
                fill: false,
            },
            {
                label: 'Z',
                borderColor: 'rgba(0,0,255,0.8)',
                backgroundColor: 'rgba(0,0,255,0.8)',
                fill: false,
            },
        ]
    },
    options: {
        responsive: true,
        title:{
            display: true,
            text: 'Test chart'
        },
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Time'
                }
            }],
            yAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Value'
                }
            }]
        }
    }
};
var label = 0;

window.onload = function() {
    var ctx = document.getElementById('canvas').getContext('2d');
    window.test_chart = new Chart(ctx, chart_config);
}

function add_data_to_chart(data) {
    if (data.sensors.gyro.x.length == 0) {
        return;
    }
    chart_config.data.labels.push(label++);
    chart_config.data.datasets[0].data.push(data.sensors.gyro.x[0]);
    chart_config.data.datasets[1].data.push(data.sensors.gyro.y[0]);
    chart_config.data.datasets[2].data.push(data.sensors.gyro.z[0]);
    window.test_chart.update();
}

function clear_chart() {
    chart_config.data.labels = [];
    chart_config.data.datasets.forEach( (dataset) => {
        dataset.data = [];
    });
}