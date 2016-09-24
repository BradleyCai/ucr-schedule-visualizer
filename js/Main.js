// Objects
var schedule;
var parser = new CourseParser();
var quarterDates;

// Booleans
var HTML5 = false; // If this browser supports HTML5
var made = false; // If the schedule has been made and drawn yet
var unrecognized = false;

// Document input
var input = document.getElementById('regex');

// rawSchedule cookie
var rawSchedule = Cookies.get("rawSchedule");

// courseList
var courseList;

// Check for HTML5 compatability
if (window.File && window.FileReader && window.FileList) {
    HTML5 = true;
} else {
    alert("This browser isn't fully supported!");
}

if (rawSchedule !== undefined) {
    made = true;
    $('#regex').hide(250);
    parser.createCourseList(rawSchedule);
    courseList = parser.getCourseList();
    quarterDates = new QuarterDates(courseList[0].year, courseList[0].quarter);
    schedule = new Schedule(rawSchedule, courseList, quarterDates.getQuarterEndDate());
    schedule.build();
}

input.onkeyup = function () {
    //Quick check if input is a schedule
    if (this.value.match(parser.getRegex()) && !made) {
        unrecognized = false;
        $('#unrecognized').hide(250);
        $('#unrecognized').remove();
        made = true;
        $('#regex').hide(250);
        rawSchedule = this.value + "\n";
        parser.createCourseList(rawSchedule);
        courseList = parser.getCourseList();
        quarterDates = new QuarterDates(courseList[0].year, courseList[0].quarter);
        schedule = new Schedule(rawSchedule, courseList, quarterDates.getQuarterEndDate());
        schedule.build();
    }
    else if (this.value.length > 20 && !unrecognized && !this.value.match(parser.getRegex())) {
        var unrecognizedString = '<div class="container" id ="unrecognized"><p class = "alert alert-error"><strong>Something went wrong!</strong> We were not able to recognize your schedule. Please email us with your schedule so that we can take a closer look. Sorry about that.';

        $(".table-space").before(unrecognizedString);
        unrecognized = true;
    }
    else if (this.value.length < 20 && unrecognized) {
        unrecognized = false;
        $('#unrecognized').hide(250);
        $('#unrecognized').remove();
    }
};

//$(".centered").append("<button class = 'btn' id = 'cal'>Export to Google Calender</button>");
