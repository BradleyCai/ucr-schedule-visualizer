var HTML5 = false; // If browser supports HTML5
var made = false; // If the schedule has been made and drawn yet
var parser = new CourseParser();
var schedule;
var input = document.getElementById('regex');

if (window.File && window.FileReader && window.FileList) {
    HTML5 = true;
} else {
    alert("This browser isn't fully supported!");
}

input.onkeyup = function() {
    //Quick check if input is a schedule
    if(this.value.match(parser.getRegex()) && !made) {
        made = true;
        $('#regex').hide(250);
        parser.createCourseList(this.value + "\n");
        schedule = new Schedule(parser.getCourseList());
        schedule.createHourList();
        schedule.injectTable();
        schedule.drawCanvasTable(150, 25);
        console.log(schedule.courseList);
        console.log(schedule.hourList);
        console.log(parser.noShowList);
    }
};

//$(".centered").append("<button class = 'btn' id = 'cal'>Export to Google Calender</button>");
