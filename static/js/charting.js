var chart_config = {
    type: 'line',
    data: {
        datasets: [{
            label: 'X',
            fill: false,
            borderColor: window.chartColors.red,
        }]
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
    window.testChart = new Chart(ctx, chart_config);
}

function add_data_to_chart(data) {
    console.log(label);
    chart_config.data.labels.push(label++);
    chart_config.data.datasets.forEach((dataset) => {
        dataset.data.push(data.sensors.gyro.x[0]);
    });
    window.testChart.update();
}