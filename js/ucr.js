/**
 * Class to represent a course. Should be used in a list to represent a schedule.
 * Has functions avaliable to manipulate the data and present things in different ways.
 * 
 * @constructor 
 * @author Bradley Cai
 */
function Course(quarter, name, nameID, bldg, room, gt, units,
                hour1, min1, hour2, min2, days) {
    
    //General information
    this.quarter = quarter; //written as a string in the format of "season####"
    this.name = name;
    this.nameID = nameID; //ID written under the name of the course. (ex. CHEM-001A-060)
    this.bldg = bldg; //String of the bldg
    this.room = room; //String of room number
    this.gt = gt; //GT - Grade type. No one knows what this is
    this.units = units; //Expressed as a double
    
    //Time information
    this.hour1 = hour1; //Hour class begins. Integer between 0-23
    this.min1 = min1; //Integer between 0-59
    this.hour2 = hour2; //Hour when class ends.
    this.min2 = min2; 
    
    //Array information
    this.blocks = 2*(this.hour2 - this.hour1) - (this.min2 - this.min1)/30; //How many 30 minute blocks it takes (ex 60 is 2 blocks)
    this.duration = 30 * this.blocks; //Duration of class in minutes (ex. 60 for 60 minutes)
    this.pos = ((this.hour1 * 60 + this.min1) - 420)/30; //Position on the hourList
    this.days = [false, false, false, false, false, false]; //Array of days as booleans.
    
    for(var i = 0; i < days.length; i++) {
        switch(days.charAt(i)) {
            case "M":
                this.days[0] = true;
                break;
            case "T":
                this.days[1] = true;
                break;
            case "W":
                this.days[2] = true;
                break;
            case "R":
                this.days[3] = true;
                break;
            case "F":
                this.days[4] = true;
                break;
            case "S":
                this.days[5] = true;
                break;
        }
    }
}
var courseList = 0;
var hourList = 0;

/**
 * Test function to fill an array with dummy courses.
 *
 * @return - A fake courseList of courses. 
 */
function createTestCourses() {
    
    var list = new Array();
    
    /*Example courses. Will be filled from user input in the final version */
    list.push(new Course("FALL", "INTRO: CS FOR SCI,MATH&ENGR I", "CS -010 -001", "BRNHL", "A125", "None", 4,
                    9, 0, 10, 0, "MWF"));
    list.push(new Course("FALL", "INTRO: CS FOR SCI,MATH&ENGR I", "CS -010 -001", "BRNHL", "A125", "None", 4,
                    15, 30, 17, 0, "TR"));
    
    return list;
}

/**
 * Creates a 2D array whose rows are time in 30 minute blocks and columns days of the week.
 * The spot on a calender where the courses takes place in time on a certain day will fill
 * that postion on the array.
 * 
 */
function createHourList() {             
    //Initialize a 2-D array. Each item within the array is an array.
    hourList = new Array(32)
    for (var i = 0; i < 32; i++) {
        hourList[i] = new Array(6);
    }
    
    for (var c = 0; c < courseList.length; c++) { //for each course
        var current = courseList[c];
        for (var day = 0; day < current.days.length; day++) { //for each day of the week
            if (current.days[day] == true) {
                //console.log(courseList[c].pos + " " + day);
                for (var b = 0; b < current.blocks; b++) {//for each block
                    
                    hourList[current.pos + b][day] = courseList[c];
                }
            }
        }
    }
}

/**
 * Creates a string for the innerHTML element of the table. You can view the html in the console log
 * 
 * More is explained inside.
 *
 */
function createTableString() {
    //This creates the first row of days
    var tableString = 
"<table class='pure-table'>\n \
    <thead>\n \
        <tr>\n \
            <th></th>\n \
            <th>Monday</th>\n \
            <th>Tuesday</th>\n \
            <th>Wednesday</th>\n \
            <th>Thursday</th>\n \
            <th>Friday</th>\n \
            <th>Saturday</th>\n \
        </tr>\n \
    </thead>\n \
    <tbody>\n";
    
    //This creates the body of the table
    var hour = 0;
    for (var row = 0; row < 32; row++) { //for each tr/row (700 730 800 etc). 32 is the amount of rows. See blocks
        
        //Starts off the row with an hour ID to keep things readable
        tableString += "<tr id = '" + (row * 30 + 420)/60 + "'>\n";
        
        //This is the 12 hour clock mechanism
        if (row < 11) {
            hour = (row * 30 + 420)/60;
        }
        else {
            hour = (row * 30 + 420)/60 - 12;
        }
        
        //This creates the first column of times and adds AM or PM based on time of day
        if (row % 2 == 0) { //To make each rowspan 2 time column
            if (Math.floor(row/15) == 0) {
                tableString += "<td rowspan='2'><strong>" + hour + "AM</strong></td>\n" }
            else {
                tableString += "<td rowspan='2'><strong>" + hour + "PM</strong></td>\n" }
        }
        
        //This creates the courses in the table
        for (var col = 0; col < 6; col++) { // for each td/day (mon - sat = 6)
            courseAtI = hourList[row][col];
            
            //This displays the course info per course, instead of per block
            if (!(courseAtI == null)) {
                if (hourList[row - 1][col] == null) {
                    var popoutString;
                    switch (courseAtI.blocks) {
                        case 1:
                            tableString += "<td class='rspan' rowspan='" + courseAtI.blocks + "'>" + courseAtI.nameID + "</td>\n";
                            break;
                        case 2:
                            tableString += "<td class='rspan' rowspan='" + courseAtI.blocks + "'>" + courseAtI.nameID
                            + "<br>" + courseAtI.duration + " minutes</td>\n";
                            break;
                        default:
                            tableString += "<td class='rspan' rowspan='" + courseAtI.blocks + "'>" + courseAtI.nameID
                            + "<br>" + courseAtI.duration + " minutes<br>" + courseAtI.bldg + " "
                            + courseAtI.room + "</td>\n"
                            break;
                    }
                    
                }
            }
            else {
                tableString += "<td></td>\n";
            }
        }
    }
    tableString += "</table>";
    return tableString;
}

/**
 * This will find the div with an ID of "table-space" and then insert the innerHTML that createTableString() made.
 * Will also display the tableString on the console log
 *
 */
function createTable(tableString) {
    var tableSpace = document.getElementById("table-space");

    tableSpace.innerHTML = tableString;
    console.log(tableString);
}