/**
 * Class for storing the courseList as a 2D hour array.
 *
 * Has functions to be able to create the hourList instance variable, draw the table as a
 * canvas, drawCanvasTable(), inject the table HTML into the document, injectTable(),
 * to give the table course links popovers, createPopovers(), and some accessor functions.
 *
 * @author Bradley
 */
function Schedule(courseList) {
    this.courseList = courseList;
    this.hourList = -1;
    this.canvas = document.createElement('canvas');
    this.tableString = -1;

    /**
     * Creates a 2D array whose rows are time in 30 minute blocks and columns days of the week.
     * The spot on a calender where the courses takes place in time on a certain day will fill
     * that postion on the array.
     *
     * @param courseList - A list of courses
     * @return hourList - A 2D array hour list
     */
    this.createHourList = function() {
        var hasConflict = false;
        //Initialize a 2-D array. Each item within the array is an array.
        this.hourList = new Array(32);
        for (var i = 0; i < 32; i++) {
            this.hourList[i] = new Array(6);
        }

        for (var c = 0; c < this.courseList.length; c++) { //for each course
            var courseAtI = this.courseList[c];
            courseAtI.setIndex(c);

            for (var day = 0; day < courseAtI.days.length; day++) { //for each day of the week
                if (courseAtI.days[day] === true) {
                    //console.log(courseList[c].pos + " " + day);
                    for (var b = 0; b < courseAtI.blocks; b++) {//for each block
                        if (this.hourList[courseAtI.pos + b][day] == null) { // short hand for: if (typeof hourList[courseAtI.pos + b][day] === 'undefined' && hourList[courseAtI.pos + b][day] === null).
                                this.hourList[courseAtI.pos + b][day] = this.courseList[c];
                        }
                        else {
                            if (!hasConflict) {
                                var conflictString = '<div class="container" id = "conflict"><p class = "alert alert-error"><strong>Two or more courses appear to be scheduled at the same time. You might want to check that over. </strong>';

                                $(".table-space").before(conflictString);
                                hasConflict = true;
                            }
                        }

                    }
                }
            }
        }
    };

    this.injectButtons = function(canvas) {
        $(".centered").append("<button class = 'btn' id = 'imageDL'>Download as Image</button>");
        $(".centered").append("<button class = 'btn' id = 'reload'>Visualize Again</button>");

        $("#reload").click(function() {
            made = false;
            document.getElementById("regex").value = "";
            $('#regex').show(250);
            $('.pure-table').hide(250);
            $('#imageDL').hide(250);
            $('#reload').hide(250);
            $('#noShow').hide(250);
            $('#conflict').hide(250);

            $('.pure-table').remove();
            $('#imageDL').remove();
            $('#reload').remove();
            $('#noShow').remove();
            $('#conflict').remove();
        });

        $("#imageDL").click(function() {
            canvas.toBlob(function(blob) {
                saveAs(blob, "UCR-Schedule-Visualized.png");
            });
        });
    };

    this.drawCanvasTable = function(cellWidth, cellHeight) {
        var canvas = this.canvas;
        var offset = 100; //Sets the table down (offset) amount of pixels. Used for the title
        var tableWidth = cellWidth * this.hourList[0].length + cellWidth + 1;
        var tableHeight = cellHeight * this.hourList.length + cellHeight + 1 + offset;

        this.canvas.width = tableWidth;
        this.canvas.height = tableHeight;

        var context = this.canvas.getContext("2d");
        context.font = 'bold 50px "Helvetica"';
        context.textBaseline = "middle";
        context.textAlign = "center";

        var courseAtI;

        var days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
        context.fillStyle = "white";
        context.fillRect(0, 0, tableWidth, tableHeight);
        context.fillStyle = "black";
        context.fillText("UCR Schedule Visualizer", tableWidth / 2, 30);
        context.font = '18px "Helvetica"';
        context.fillText("https://waa.ai/ucrsv", tableWidth / 2, 65);
        context.font = '14px "Helvetica"';

        for (var day = 0; day < days.length; day++) { //Heh, courses for days. No? Okay ;_;
            context.rect(day * cellWidth + cellWidth + 0.5, offset + 0.5, cellWidth, cellHeight);
            context.fillText(days[day], day * cellWidth + cellWidth + cellWidth / 2, cellHeight / 2 + offset);
        }
        context.rect(0.5, offset + 0.5, cellWidth, cellHeight);

        var hour = 0;
        for (var row = 1; row < this.hourList.length + 1; row++) { //For each row (30 minute block)
            if (row % 2 == 1) {
                hour = Math.ceil(((row * 30 + 390) / 60) % 12.1);
                context.rect(0.5, row * cellHeight + offset + 0.5, cellWidth, cellHeight * 2);
                if (Math.floor(row / 10) === 0) {
                    context.fillText(hour + "AM", 0.5 + cellWidth / 2, row * cellHeight + cellHeight + offset + 0.5);
                }
                else {
                    context.fillText(hour + "PM", 0.5 + cellWidth / 2, row * cellHeight + cellHeight + offset + 0.5);
                }

            }

            var location = -1;
            for (var col = 1; col < this.hourList[0].length + 1; col++) { //For each day (Mon-Sat)
                courseAtI = this.hourList[row - 1][col - 1];

                if (courseAtI !== undefined) {

                    if (this.hourList[row - 2][col - 1] != courseAtI) {
                        if (courseAtI.bldg === "TBA" && courseAtI.room === "TBA") {
                            location = "TBA";
                        }
                        else {
                            location = courseAtI.bldg + " " + courseAtI.room;
                        }

                        switch (courseAtI.blocks) {
                            case 1:
                                context.rect(col * cellWidth + 0.5, row * cellHeight + 0.5 + offset, cellWidth, cellHeight);
                                context.fillText(courseAtI.nameID, col * cellWidth + cellWidth / 2, row * cellHeight + cellHeight / 2 + offset);
                                break;
                            case 2:
                                context.fillStyle = "#E6E6E6";
                                context.fillRect(col * cellWidth + 0.5, row * cellHeight + 0.5 + offset, cellWidth, cellHeight * 2);
                                context.fillStyle = "black";
                                context.strokeRect(col * cellWidth + 0.5, row * cellHeight + 0.5 + offset, cellWidth, cellHeight * 2);
                                context.fillText(courseAtI.nameID, col * cellWidth + cellWidth / 2, row * cellHeight + cellHeight / 2 + offset);
                                context.fillText(location, col * cellWidth + cellWidth / 2, row * cellHeight + cellHeight + cellHeight / 2 + offset);
                                break;
                            default:
                                context.fillStyle = "#E6E6E6";
                                context.fillRect(col * cellWidth + 0.5, row * cellHeight + 0.5 + offset, cellWidth, cellHeight * courseAtI.blocks);
                                context.fillStyle = "black";
                                context.strokeRect(col * cellWidth + 0.5, row * cellHeight + 0.5 + offset, cellWidth, cellHeight * courseAtI.blocks);
                                context.fillText(courseAtI.nameID, col * cellWidth + cellWidth / 2, row * cellHeight + cellHeight * courseAtI.blocks / 2 - cellHeight + offset);
                                context.fillText(courseAtI.duration + " minutes", col * cellWidth + cellWidth / 2, row * cellHeight + cellHeight * courseAtI.blocks / 2 + offset);
                                context.fillText(location, col * cellWidth + cellWidth / 2, row * cellHeight + cellHeight * courseAtI.blocks / 2 + cellHeight + offset);
                                break;
                        }
                    }
                }
                else {
                    context.rect(col * cellWidth + 0.5, row * cellHeight + 0.5 + offset, cellWidth, cellHeight);
                }
            }
        }
        context.stroke();

        this.injectButtons(canvas);
    };

    /**
     * Creates a string for the innerHTML element of the table. You can view the html in the console log
     *
     * More is explained inside.
     *
     */
    this.createTableString = function () {
        //This creates the first row of days
        this.tableString = "<table class='pure-table'>\n <thead> \n<tr> \n<th></th> \n<th>Monday</th> \n<th>Tuesday</th> \n<th>Wednesday</th> \n<th>Thursday</th> \n<th>Friday</th> \n<th>Saturday</th> \n</tr> \n</thead> \n<tbody>\n";

        //This creates the body of the table
        var hour = 0;
        var popoutString = -1;
        var location = -1;
        var courseAtI;
        for (var row = 0; row < 32; row++) { //for each tr/row (700 730 800 etc). 32 is the amount of rows. See blocks

            //Starts off the row with an hour ID to keep things readable
            this.tableString += "<tr id = '" + (row * 30 + 420) / 60 + "'>\n";

            //This is the 12 hour clock mechanism
            hour = Math.ceil(((row * 30 + 420) / 60) % 12.1);

            //This creates the first column of times and adds AM or PM based on time of day
            if (row % 2 === 0) { //To make each rowspan 2 time column
                if (Math.floor(row / 10) === 0) {
                    this.tableString += "<td rowspan='2'><strong>" + hour + "AM</strong></td>\n";
                }
                else {
                    this.tableString += "<td rowspan='2'><strong>" + hour + "PM</strong></td>\n";
                }
            }

            //This creates the courses in the table
            for (var col = 0; col < 6; col++) { // for each td/day (mon - sat = 6)
                courseAtI = this.hourList[row][col];

                //This displays the course info per course, instead of per block
                if (courseAtI !== undefined) {
                    if (this.hourList[row - 1][col] !== courseAtI) {
                        popoutString = "<td class='rspan' rowspan='" + courseAtI.blocks + "'>" +
                            "<a href='' onclick='return false;' " +
                            "class='course" + courseAtI.index + "'>\n";

                        if (courseAtI.bldg === "TBA" && courseAtI.room === "TBA") {
                            location = "TBA";
                        }
                        else {
                            location = courseAtI.bldg + " " + courseAtI.room;
                        }

                        switch (courseAtI.blocks) {
                            case 1:
                                this.tableString += popoutString + courseAtI.nameID + "</a></td>\n";
                                break;
                            case 2:
                                this.tableString += popoutString + courseAtI.nameID +
                                    "<br>" + location + "</a></td>\n";
                                break;
                            default:
                                this.tableString += popoutString + courseAtI.nameID + "<br>" + courseAtI.duration + " minutes<br>" +
                                    location + "</a></td>\n";
                                break;
                        }
                    }
                }
                else {
                    this.tableString += "<td></td>\n";
                }
            }
        }
        this.tableString += "</tbody>\n</table>";
    };

    /**
     * This will find the div with an ID of "table-space" and then insert the innerHTML that createTableString() made.
     * Will also display the tableString on the console log
     *
     */
    this.injectTable = function () {
        var tableSpace = document.getElementById("table-space");
        this.createTableString();

        loadBuildingNames();

        tableSpace.innerHTML = this.tableString;

        //console.log(this.tableString);
    };

    this.createPopovers = function () {
        var courseAtI;
        for (var c = 0; c < this.courseList.length; c++) {
            courseAtI = this.courseList[c];

            var location = getBuildingLocation(courseAtI.bldg, courseAtI.room);

            $('.course' + c).popover({
                title: courseAtI.name,
                content: "<strong>Times: </strong>" + courseAtI.times +
                " <br><strong>Building:</strong> " + courseAtI.bldg +
                " <br><strong>Room:</strong> " + courseAtI.room +
                " <br><strong>GT:</strong> " + courseAtI.gt +
                " <br><strong>Location:</strong> " + location,
                html: true,
                animation: true,
                trigger: "focus"
            });
        }
    };

    this.getCourseList = function () {
        return this.courseList;
    };

    this.getHourList = function () {
        return this.hourList;
    };

    this.getCanvas = function () {
        return canvas;
    };

    this.getTableString = function () {
        return this.tableString;
    };

    this.getGud = function () {
        var powerLevel = 9001;
        return powerLevel;
    };
}
