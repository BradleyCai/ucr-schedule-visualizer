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
    this.createHourList = function () {
        //Initialize a 2-D array. Each item within the array is an array.
        this.hourList = new Array(32);
        for (var i = 0; i < 32; i++) {
            this.hourList[i] = new Array(6);
        }

        for (var c = 0; c < this.courseList.length; c++) { //for each course

            var current = this.courseList[c];
            current.setIndex(c);
            for (var day = 0; day < current.days.length; day++) { //for each day of the week
                if (current.days[day] === true) {
                    //console.log(courseList[c].pos + " " + day);
                    for (var b = 0; b < current.blocks; b++) {//for each block
                        this.hourList[current.pos + b][day] = this.courseList[c];
                    }
                }
            }
        }
    };

    // TODO: split into multiple functions
    this.drawCanvasTable = function (numCols, numRows) {
        var canvas = this.canvas;
        var offset = 100; //Sets the table down (offset) amount of pixels. Used for the title
        var tableWidth = numCols * this.hourList[0].length + numRows + 1;
        var tableHeight = numRows * this.hourList.length + numRows + 1 + offset;

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
            context.rect(day * numCols + numCols + 0.5, offset + 0.5, numCols, numRows);
            context.fillText(days[day], day * numCols + numCols + numCols / 2, numRows / 2 + offset);
        }
        context.rect(0.5, offset + 0.5, numCols, numRows);

        var hour = 0;
        for (var row = 1; row < this.hourList.length + 1; row++) { //For each row (30 minute block)
            if (row % 2 == 1) {
                hour = Math.ceil(((row * 30 + 420) / 60) % 12.1);
                context.rect(0.5, row * numRows + offset + 0.5, numCols, numRows * 2);
                if (Math.floor(row / 10) === 0) {
                    context.fillText(hour + "AM", 0.5 + numCols / 2, row * numRows + numRows + offset + 0.5);
                }
                else {
                    context.fillText(hour + "PM", 0.5 + numCols / 2, row * numRows + numRows + offset + 0.5);
                }

            }

            for (var col = 1; col < this.hourList[0].length + 1; col++) { //For each day (Mon-Sat)
                courseAtI = this.hourList[row - 1][col - 1];

                if (courseAtI != null) { // short hand for: if (typeof courseAtI !== 'undefined' && courseAtI !== null).
                    if (this.hourList[row - 2][col - 1] != courseAtI) {
                        switch (courseAtI.blocks) {
                            case 1:
                                context.rect(col * numCols + 0.5, row * numRows + 0.5 + offset, numCols, numRows);
                                context.fillText(courseAtI.nameID, col * numCols + numCols / 2, row * numRows + numRows / 2 + offset);
                                break;
                            case 2:
                                context.fillStyle = "#E6E6E6";
                                context.fillRect(col * numCols + 0.5, row * numRows + 0.5 + offset, numCols, numRows * 2);
                                context.fillStyle = "black";
                                context.strokeRect(col * numCols + 0.5, row * numRows + 0.5 + offset, numCols, numRows * 2);
                                context.fillText(courseAtI.nameID, col * numCols + numCols / 2, row * numRows + numRows / 2 + offset);
                                context.fillText(courseAtI.bldg + " " + courseAtI.room, col * numCols + numCols / 2, row * numRows + numRows + numRows / 2 + offset);
                                break;
                            default:
                                context.fillStyle = "#E6E6E6";
                                context.fillRect(col * numCols + 0.5, row * numRows + 0.5 + offset, numCols, numRows * courseAtI.blocks);
                                context.fillStyle = "black";
                                context.strokeRect(col * numCols + 0.5, row * numRows + 0.5 + offset, numCols, numRows * courseAtI.blocks);
                                context.fillText(courseAtI.nameID, col * numCols + numCols / 2, row * numRows + numRows * courseAtI.blocks / 2 - numRows + offset);
                                context.fillText(courseAtI.duration + " minutes", col * numCols + numCols / 2, row * numRows + numRows * courseAtI.blocks / 2 + offset);
                                context.fillText(courseAtI.bldg + " " + courseAtI.room, col * numCols + numCols / 2, row * numRows + numRows * courseAtI.blocks / 2 + numRows + offset);
                                break;
                        }
                    }
                }
                else {
                    context.rect(col * numCols + 0.5, row * numRows + 0.5 + offset, numCols, numRows);
                }
            }
        }
        context.stroke();

        $(".centered").append("<button class = 'btn' id = 'imageDL'>Download as an Image</button>");

        $("#imageDL").click(function () {
            canvas.toBlob(function (blob) {
                saveAs(blob, "schedule.png");
            });
        });
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
                if (courseAtI != null) { //short hand for: if (typeof courseAtI !== 'undefined' && courseAtI !== null).
                    if (this.hourList[row - 1][col] !== courseAtI) {
                        popoutString = "<td class='rspan' rowspan='" + courseAtI.blocks + "'>" +
                            "<a href='' onclick='return false;' " +
                            "class='course" + courseAtI.index + "'>\n";

                        switch (courseAtI.blocks) {
                            case 1:
                                this.tableString += popoutString + courseAtI.nameID + "</a></td>\n";
                                break;
                            case 2:
                                this.tableString += popoutString + courseAtI.nameID +
                                    "<br>" + courseAtI.bldg + " " + courseAtI.room + "</a></td>\n";
                                break;
                            default:
                                this.tableString += popoutString + courseAtI.nameID + "<br>" + courseAtI.duration + " minutes<br>" +
                                    courseAtI.bldg + " " + courseAtI.room + "</a></td>\n";
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

        tableSpace.innerHTML = this.tableString;

        loadBuildingNames();
        //console.log(this.tableString);
    };

    this.createPopovers = function () {
        var courseAtI;
        for (var c = 0; c < this.courseList.length; c++) {
            courseAtI = this.courseList[c];

            //This block will give "None" to empty variables in a course
            var gt = (courseAtI.gt === "") ? "None" : courseAtI.gt;
            var days = (courseAtI.days === "") ? "None" : courseAtI.days;
            var bldg = (courseAtI.bldg === "") ? "None" : courseAtI.bldg;
            var room = (courseAtI.room === "") ? "None" : courseAtI.room;
            var locat = getBuildingLocation(bldg, room);

            $('.course' + c).popover({
                title: courseAtI.name,
                content: "<strong>Times: </strong>" + courseAtI.times +
                " <br><strong>Building:</strong> " + bldg +
                " <br><strong>Room:</strong> " + room +
                " <br><strong>GT:</strong> " + gt +
                " <br><strong>Location:</strong> " + locat,
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
