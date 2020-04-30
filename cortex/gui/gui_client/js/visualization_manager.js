class VisualizationManager {
  // Constant Section
  #MY_CONST = "IM CONST"; // TODO REMOVE
  // Variables Section
  // Data Section
  #arrFeelingsData = undefined;
  #dictSnapshotsDictionary = undefined;
  // Snapshot sentinels variables section
  #nLastSnapshotValue = undefined;
  #nLastSnapshotID = undefined;
  // Charts variables section
  #bcTranslationBarChart = undefined;
  #bcRotatationBarChart = undefined;

  draw_feelings_multiline_graph(arrFeelingsData) {
    // Binding function for attaching current object to method upon callback
    var bind = function (toObject, methodName) {
      return function (x) {
        toObject[methodName](x);
      };
    };
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
        exhaustion: "#000000",
        happiness: "green",
      },
    };
    // Draw multiline graph based on configuration and data
    multiline_graph(arrFeelingsData, dictConfiguration);
  }

  static convert_snapshots_data_to_dictionary(dSnapshotsData) {
    // Constant Definition
    const SNAPSHOT_UUID_NAME = "snapshot_uuid";
    const SNAPSHOT_DATETIME_NAME = "datetime";
    const NON_JSON_SNAPSHOT_FIELDS = [
      SNAPSHOT_UUID_NAME,
      SNAPSHOT_DATETIME_NAME,
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
        dictCurrentSnapshot[SNAPSHOT_UUID_NAME]
      ] = dictCurrentSnapshot;
    }
    // Return snapshots dictionary
    return dictSnapshotsDictionary;
  }

  static extract_feelings_from_snapshots(dictSnapshotsDictionary) {
    // Constant Definition
    const SNAPSHOT_UUID_NAME = "snapshot_uuid";
    const SNAPSHOT_DATETIME_NAME = "datetime";
    const SNAPSHOT_USER_FEELINGS_NAME = "user_feelings";
    // Variable Definition
    var arrFeelingsData = [];
    // Code Section
    // Going over all snapshots dictionary and extracting user feelings
    for (var kSnapshotKey in dictSnapshotsDictionary) {
      // OUR GOAL:
      // { "datetime": 20111001, "snapshot_uuid": 322, "hunger": 50.4, "thirst": 62.7, "exhaustion": 72.2, "happiness": 72.2 }
      var sSnapshot = dictSnapshotsDictionary[kSnapshotKey];
      var dictSnapshotUserFeelings = {};
      dictSnapshotUserFeelings[SNAPSHOT_UUID_NAME] =
        sSnapshot[SNAPSHOT_UUID_NAME];
      dictSnapshotUserFeelings[SNAPSHOT_DATETIME_NAME] =
        sSnapshot[SNAPSHOT_DATETIME_NAME];
      dictSnapshotUserFeelings = Object.assign(
        {},
        dictSnapshotUserFeelings,
        sSnapshot[SNAPSHOT_USER_FEELINGS_NAME]
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
    // Feelings initialization
    this.draw_feelings_multiline_graph(this.arrFeelingsData);
    // Bar charts initialization
    this.bcTranslationBarChart = bar_chart(
      "bar_chart_translation",
      "Translation",
      ["x", "y", "z"]
    );
    this.bcRotatationBarChart = bar_chart("bar_chart_rotation", "Rotation", [
      "x",
      "y",
      "z",
      "w",
    ]);
  }

  // Update Current Snapshot Method
  update_to_current_snapshot(x) {
    // TODO : remove mock
    var randomArray = function (length, max) {
      return Array.apply(null, Array(length)).map(function () {
        return (
          Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * max) / max
        );
      });
    };

    // Get current snapshot
    this.nCurrentSnapshotID = x[0];
    this.nCurrentSnapshotValue = x[1].getTime();
    // If current snapshot is diffrent from last snapshot
    if (this.nLastSnapshotID != this.nCurrentSnapshotID) {
      var sSnapshot = this.dictSnapshotsDictionary[this.nCurrentSnapshotID];
      // Images update
      $("#color_image").attr("src", sSnapshot["color_image"].data_uri);
      $("#depth_image").attr("src", sSnapshot["depth_image"].data_uri);
      // TODO : Fields can be accessed via globalThis.class_field
      // Bar charts update
      var pPose = sSnapshot["pose"];
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
    // Update snapshot sentinels
    this.nLastSnapshotID = this.nCurrentSnapshotID;
    this.nLastSnapshotValue = this.nCurrentSnapshotValue;
  }
}
