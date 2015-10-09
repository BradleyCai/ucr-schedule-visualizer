/**
 * Class to represent a course. Should be used in a list to represent a schedule.
 * Has functions avaliable to manipulate the data and present things in different ways.
 * 
 * @constructor 
 * @author Bradley Cai
 */
function Course(quarter, name, nameId, bldg, room, gt, units,
                hour1, min1, hour2, min2, days) {
    
    
    //General information
    this.quarter = quarter; //written as a string in the format of "season####"
    this.name = name;
    this.nameId = nameId; //ID written under the name of the course. (ex. CHEM-001A-060)
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
 * Test function to fill courseList with dummy courses
 *
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
function createHourList() {             
    //Initialize a 2-D array. Each item within the array is an array.
    hourList = new Array(30)
    for (var i = 0; i < 30; i++) {
        hourList[i] = new Array(6);
    }
    
    for (var c = 0; c < courseList.length; c++) { //for each course
        for (var day = 0; day < courseList[c].days.length; day++) { //for each day of the week
            if (courseList[c].days[day] == true) {
                //console.log(courseList[c].pos + " " + day);
                hourList[courseList[c].pos][day] = courseList[c]; }
        }
    }
}

function createTable() {
    var hourList = document.getElementById("table-space");
    
    hourList.innerHTML = "<table class='pure-table'> \
                    <thead> \
                        <tr> \
                            <th></th> \
                            <th>Monday</th> \
                            <th>Tuesday</th> \
                            <th>Wednesday</th> \
                            <th>Thursday</th> \
                            <th>Friday</th> \
                            <th>Saturday</th> \
                        </tr> \
                    </thead>";
    
    
}
courseList = createTestCourses();
createHourList();