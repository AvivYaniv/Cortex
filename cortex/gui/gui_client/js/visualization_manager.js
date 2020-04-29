function VisualizationManager() {
  // Variables Section
  // Data Section
  var dFeelingsData = undefined;
  // Snapshot sentinels variables section
  var nLastSnapshotValue = undefined;
  var nLastSnapshotID = undefined;
  // Charts variables section
  var bcTranslationBarChart = undefined;
  var bcRotatationBarChart = undefined;

  // TODO : remove mock
  randomArray = function (length, max) {
    return Array.apply(null, Array(length)).map(function () {
      return (
        Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * max) / max
      );
    });
  };

  draw_feelings_multiline_graph = function (dFeelingsData) {
    // Initialize feelings data configuration
    var dictConfiguration = {
      mouse_legend_date_format: "", // " - %d/%m/%Y %H:%M:%S"
      x_axis_date_format: "%d/%m/%Y %H:%M",
      y_axis_legend: "Intensity",
      y_axis_extent: [40, 100],
      element_id: "user_feelings",
      mouse_moving_callback:
        window.vmVisualizationManager.update_to_current_snapshot,
      input_date_format: "%Y%m%d",
      id_column_name: "snapshot_uuid",
      date_colum_name: "datetime",
      show_lines_rect_legend: false,
      predefined_colors_dictionary: {
        hunger: "#FD4F2A",
        thirst: "#629EBB",
        exhaustion: "#000000",
        happiness: "green",
      },
    };
    // Draw multiline graph based on configuration and data
    multiline_graph(dFeelingsData, dictConfiguration);
  };

  draw_feelings_radar_chart = function () {
    //Data
    var d = [
      [
        { axis: "tx", value: Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 100) / 100 },
        { axis: "ty", value: Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 100) / 100 },
        { axis: "tz", value: Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 100) / 100 },
        { axis: "tw", value: Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 100) / 100 },
      ],
    ];

    //Options for the Radar chart, other than default
    var mycfg = {
      w: 200,
      h: 200,
      ExtraWidthX: 0,
      ExtraWidthY: 0,
      maxValue: 1,
      levels: 10,
    };

    // Draw the Radar chart
    RadarChart.draw("#radar_chart", d, mycfg);
  };

  // Methods Section
  // Initialization Method
  this.initialize = function (dFeelingsData) {
    // Code Section
    // Initialize feelings data
    dFeelingsData = dFeelingsData;
    // Feelings initialization
    draw_feelings_multiline_graph(dFeelingsData);
    // Bar charts initialization
    bcTranslationBarChart = bar_chart("bar_chart_translation", "Translation", [
      "x",
      "y",
      "z",
      "w",
    ]);
    bcRotatationBarChart = bar_chart("bar_chart_rotation", "Rotation", [
      "x",
      "y",
      "z",
    ]);
  };
  // Update Current Snapshot Method
  this.update_to_current_snapshot = function (x) {
    // Get current snapshot
    nCurrentSnapshotID = x[0];
    nCurrentSnapshotValue = x[1].getTime();
    // If current snapshot is diffrent from last snapshot
    if (nLastSnapshotID != nCurrentSnapshotID) {
      // Images update
      var urlColorImage =
        "https://i.picsum.photos/id/" +
        parseInt(nCurrentSnapshotID) +
        "/200/300.jpg";
      $("#color_image").attr("src", urlColorImage);
      // Radar chart update
      var xx = globalThis.dFeelingsData;
      draw_feelings_radar_chart();
      // Bar charts update
      bcTranslationBarChart.data.datasets[0].data = randomArray(4, 100.0);
      bcTranslationBarChart.update();
      bcRotatationBarChart.data.datasets[0].data = randomArray(3, 100.0);
      bcRotatationBarChart.update();
    }
    // Update snapshot sentinels
    nLastSnapshotID = nCurrentSnapshotID;
    nLastSnapshotValue = nCurrentSnapshotValue;
  };
}
