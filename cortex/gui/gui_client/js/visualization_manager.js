class VisualizationManager {  

  draw_feelings_multiline_graph(arrFeelingsData) {
    // In Binding callback to current object
    // as in JavaScript function is not defaultly binded
    var registerd_mouse_move_callback = bind(
      this,
      "update_to_current_snapshot"
    );
    // Initialize feelings data configuration
    var dictConfiguration = {
      mouse_legend_date_format: "", // " - %d/%m/%Y %H:%M:%S"
      x_axis_date_format: "%d/%m/%Y %H:%M:%S",
      y_axis_legend: "Intensity",
      y_axis_extent: [-1, 1],
      element_id: "user_feelings",
      mouse_moving_callback: registerd_mouse_move_callback,
      id_column_name: "snapshot_uuid",
      date_colum_name: "datetime",
      show_lines_rect_legend: false,
      predefined_colors_dictionary: {
        hunger: "#FD4F2A",
        thirst: "#629EBB",
        exhaustion: "brown",
        happiness: "green",
      },
    };
    // Draw multiline graph based on configuration and data
    multiline_graph(arrFeelingsData, dictConfiguration);
  }

  static convert_snapshots_data_to_dictionary(dSnapshotsData) {
    // Constant Definition
    const NON_JSON_SNAPSHOT_FIELDS = [
      VisualizationManager.SNAPSHOT_UUID_NAME,
      VisualizationManager.SNAPSHOT_DATETIME_NAME,
    ];
    // Variable Definition
    var dictSnapshotsDictionary = {};
    // Code Section
    // Going over all snapshots in JSON and aggregating them to dictionary
    for (
      var nSnapshotIndex = 0;
      nSnapshotIndex < dSnapshotsData.length;
      ++nSnapshotIndex
    ) {
      // Convert current snapshot from JSON to dictionary
      var dictCurrentSnapshot = JSON.parse(dSnapshotsData[nSnapshotIndex]);
      // Going over snapshot dictionary and parsing from JSON
      for (var kSnapshotField in dictCurrentSnapshot) {
        // If field is JSON type
        if (!NON_JSON_SNAPSHOT_FIELDS.includes(kSnapshotField)) {
          // Parse field from JSON
          dictCurrentSnapshot[kSnapshotField] = JSON.parse(
            dictCurrentSnapshot[kSnapshotField]
          );
        }
      }
      // Set snapshot dictionay as entry with snapshot id
      dictSnapshotsDictionary[
        dictCurrentSnapshot[VisualizationManager.SNAPSHOT_UUID_NAME]
      ] = dictCurrentSnapshot;
    }
    // Return snapshots dictionary
    return dictSnapshotsDictionary;
  }

  static extract_feelings_from_snapshots(dictSnapshotsDictionary) {
    // Variable Definition
    var arrFeelingsData = [];
    // Code Section
    // Going over all snapshots dictionary and extracting user feelings
    for (var kSnapshotKey in dictSnapshotsDictionary) {      
      var sSnapshot = dictSnapshotsDictionary[kSnapshotKey];
      var dictSnapshotUserFeelings = {};
      dictSnapshotUserFeelings[VisualizationManager.SNAPSHOT_UUID_NAME] =
        sSnapshot[VisualizationManager.SNAPSHOT_UUID_NAME];
      dictSnapshotUserFeelings[VisualizationManager.SNAPSHOT_DATETIME_NAME] =
        sSnapshot[VisualizationManager.SNAPSHOT_DATETIME_NAME];
      dictSnapshotUserFeelings = Object.assign(
        {},
        dictSnapshotUserFeelings,
        sSnapshot[VisualizationManager.SNAPSHOT_USER_FEELINGS_NAME]
      );

      // Add snapshot user feelings to the array
      arrFeelingsData.push(dictSnapshotUserFeelings);
    }
    // Return user feelings array
    return arrFeelingsData;
  }

  // Methods Section
  // Initialization Method
  constructor(dSnapshotsData) {
    // Code Section
    // Initialize snapshots dictionary
    this.dictSnapshotsDictionary = VisualizationManager.convert_snapshots_data_to_dictionary(
      dSnapshotsData
    );
    // Initialize feelings data
    this.arrFeelingsData = VisualizationManager.extract_feelings_from_snapshots(
      this.dictSnapshotsDictionary
    );     
    // Bar charts initialization
    this.bcTranslationBarChart = bar_chart(
      "bar_chart_translation",
      "Translation",
      ["x", "y", "z"],
      { scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
              min: -10,
              max: 10,
            },
          },
        ],
      }, }
    );
    this.bcRotatationBarChart = bar_chart("bar_chart_rotation", "Rotation", [
      "x",
      "y",
      "z",
      "w",
    ]);
    // Feelings initialization
    this.draw_feelings_multiline_graph(this.arrFeelingsData);   
    this.update_to_current_snapshot([Object.keys(this.dictSnapshotsDictionary)[0]]);
  }

  static date_to_string(d) {
    return d.toLocaleString();
  }

  // Update Current Snapshot Method
  update_to_current_snapshot(...params) {
    // Get current snapshot
    var cpCurrentPosition = params[0];
    this.nCurrentSnapshotID = cpCurrentPosition[0];    
    // If current snapshot is diffrent from last snapshot
    if (this.nLastSnapshotID != this.nCurrentSnapshotID) {
      var sSnapshot = this.dictSnapshotsDictionary[this.nCurrentSnapshotID];
      // Update description      
      $("#current_snapshot").text("Current Snapshot: " + VisualizationManager.date_to_string(new Date(safe_get_value_from_dictionary(sSnapshot, "datetime"))) + " (dark mouse on graph to explore)");
      // Images update      
      $("#color_image").attr("src", safe_get_value_from_dictionary(sSnapshot, "color_image").data_uri);
      $("#depth_image").attr("src", safe_get_value_from_dictionary(sSnapshot, "depth_image").data_uri);      
      // Bar charts update
      var pPose = safe_get_value_from_dictionary(sSnapshot, "pose");
      if (pPose)
      {
        this.bcTranslationBarChart.data.datasets[0].data = [
          pPose.translation_x,
          pPose.translation_y,
          pPose.translation_z,
        ];
        this.bcTranslationBarChart.update();
        this.bcRotatationBarChart.data.datasets[0].data = [
          pPose.rotation_x,
          pPose.rotation_y,
          pPose.rotation_z,
          pPose.rotation_w,
        ];
        this.bcRotatationBarChart.update();
      }
    }
    // Update snapshot sentinels
    this.nLastSnapshotID = this.nCurrentSnapshotID;    
  }
}

VisualizationManager.SNAPSHOT_UUID_NAME = "snapshot_uuid";
VisualizationManager.SNAPSHOT_DATETIME_NAME = "datetime";
VisualizationManager.SNAPSHOT_USER_FEELINGS_NAME = "user_feelings";
