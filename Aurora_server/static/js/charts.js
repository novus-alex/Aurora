$(document).ready(function(){
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var numbers_received = [];

    function getData() {
        socket.on('newnumber', function(msg) {
           numbers_received.push(msg.number)
           if (numbers_received.length >= 1){
               state1 = '<p class="status-type" style="font-size: 20px; font-family: "Noto Sans", sans-serif;">idle</p>'
               state2 = '<p class="status-type" style="font-size: 20px; font-family: "Noto Sans", sans-serif;">Bat. nominal</p>'
               state3 = '<p class="status-type" style="font-size: 20px; font-family: "Noto Sans", sans-serif;">Comms available</p>'
           } else {
               state1 = '<p class="status-type" style="font-size: 20px; font-family: "Noto Sans", sans-serif;">error</p>'
               state2 = '<p class="status-type" style="font-size: 20px; font-family: "Noto Sans", sans-serif;">Bat. N/A</p>'
               state3 = '<p class="status-type" style="font-size: 20px; font-family: "Noto Sans", sans-serif;">Comms unvailable</p>'
           }
           $('#status-state1').html(state1);
           $('#status-state2').html(state2);
           $('#status-state3').html(state3);
        return numbers_received[numbers_received.length - 1];
    })};

    var canvas = document.getElementById('chart_altimeter');
    var canvas2 = document.getElementById('chart_speed');
    var data = {
        labels: [],
        datasets: [
            {
                label: "Altimeter",
                fill: false,
                lineTension: 0.1,
                backgroundColor: "rgba(75,192,192,0.4)",
                borderColor: "rgba(75,192,192,1)",
                borderCapStyle: 'butt',
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                pointBorderColor: "rgba(75,192,192,1)",
                pointBackgroundColor: "#fff",
                pointBorderWidth: 1,
                pointHoverRadius: 0,
                pointHoverBackgroundColor: "rgba(75,192,192,1)",
                pointHoverBorderColor: "rgba(220,220,220,1)",
                pointHoverBorderWidth: 2,
                pointRadius: 0,
                pointHitRadius: 10,
                data: [],
            }
        ]
    };

    var data2 = {
        labels: [],
        datasets: [
            {
                label: "Speed",
                fill: false,
                lineTension: 0.1,
                backgroundColor: "rgba(192,75,75,0.4)",
                borderColor: "rgba(192,75,75,1)",
                borderCapStyle: 'butt',
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                pointBorderColor: "rgba(75,192,192,1)",
                pointBackgroundColor: "#fff",
                pointBorderWidth: 1,
                pointHoverRadius: 0,
                pointHoverBackgroundColor: "rgba(75,192,192,1)",
                pointHoverBorderColor: "rgba(220,220,220,1)",
                pointHoverBorderWidth: 2,
                pointRadius: 0,
                pointHitRadius: 10,
                data: [],
            }
        ]
    };

    var count = 0

    setInterval(function(){
        myLineChart.data.datasets[0].data[count] = getData();
        myLineChart.data.labels[count] = count;
        myLineChart.update();
        myLineChart2.data.datasets[0].data[count] = Math.random();
        myLineChart2.data.labels[count] = count;
        myLineChart2.update();
        count++
      ;}, 1000
    );

    var option = {
        showLines: true
    };

    var myLineChart = Chart.Line(canvas,{
        data:data,
        options:option
    });

    var myLineChart2 = Chart.Line(canvas2,{
        data:data2,
        options:option
    });
});
