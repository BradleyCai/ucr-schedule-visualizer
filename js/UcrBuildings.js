var file = "/ucr-schedule-visualizer/building_names.txt";

var buildingNames = {};

loadBuildingNames = function () {
    $.get(file, function (raw_data) {
        var data = raw_data.split("\n");
        var line;
        for (var i = 0; i < data.length; i++) {
            line = data[i].split(":");
            buildingNames[line[0]] = line[1];
        }
        schedule.createPopovers();
    });
};

getBuildingLocation = function (bldg, room) {
    var name = buildingNames[bldg];
    var url = "http://campusmap.ucr.edu/imap/index.html?loc=" + bldg;

    if (name === undefined)
        return "Unknown";

    return "<a target=\"_blank\" href=\"" + url + "\">" + name + " " + room + "</a>";
};
