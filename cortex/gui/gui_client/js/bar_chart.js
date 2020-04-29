function bar_chart(bar_chart_id, chart_label, bars_labels) {
  var data = {
    labels: bars_labels,
    datasets: [
      {
        label: chart_label,
        data: [],
        fill: false,
        backgroundColor: Array(bars_labels.length).fill("#000000"),
        borderWidth: 1,
      },
    ],
  };

  var options = {
    responsive: false,
    tooltips: {
        enabled: false
     },
     legend: {
        labels: {
          boxWidth: 0,
        }
       },
    scales: {
      yAxes: [
        {
          ticks: {
            beginAtZero: true,
            min: -1,
            max: 1,
          },
        },
      ],
    },
  };

  var ctx = document.getElementById(bar_chart_id).getContext("2d");
  var myBarChart = new Chart(ctx, {
    type: "bar",
    data: data,
    options: options,
  });

  Chart.pluginService.register({
    afterDraw: function (chartInstance) {
      var ctx = chartInstance.chart.ctx;

      // render the value of the chart above the bar
      ctx.font = Chart.helpers.fontString(
        Chart.defaults.global.defaultFontSize,
        "normal",
        Chart.defaults.global.defaultFontFamily
      );
      ctx.textAlign = "center";
      ctx.textBaseline = "bottom";

      chartInstance.data.datasets.forEach(function (dataset) {
        for (var i = 0; i < dataset.data.length; i++) {
          var model =
            dataset._meta[Object.keys(dataset._meta)[0]].data[i]._model;
          ctx.fillText(dataset.data[i], model.x, model.y - 2);
        }
      });      
    },
    beforeLayout : function (chartInstance) {
      var bars = chartInstance.chart.config.data.datasets[0];
      var data = bars.data;
      for (i = 0; i < data.length; i++) {
        bars.backgroundColor[i] = 0 < data[i] ? "green" : "red";
      }
    },
  });

  Chart.defaults.global.defaultFontColor = getComputedStyle(
    document.body
  ).color;

  return myBarChart;
}
