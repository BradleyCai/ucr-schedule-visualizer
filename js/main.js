var HTML5 = false;
var made = false;
if (window.File && window.FileReader && window.FileList) {
    HTML5 = true;
} else {
    alert("This browser isn't fully supported!");
}

var parser = new CourseParser();
var schedule;

var input = document.getElementById('regex');
$('#SearchButton').one("click", function () {
    $("#loadingMessage").css('padding-top', '6%');
});

input.onkeyup = function() {
    //Quick check if input is a schedule
    if(this.value.match(parser.getRegex()) && !made) {
        made = true;
        $('#regex').hide(250);
        parser.createCourseList(this.value);
        schedule = new Schedule(parser.getCourseList());
        schedule.createHourList();
        schedule.injectTable();
        schedule.drawCanvasTable(150, 25);
        console.log(schedule.courseList);
    }
};
