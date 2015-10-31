function CourseParser() {
    var regex = /(.*)\n\s*([A-Z]+ ?-[A-Z0-9]+ ?-[0-9]{3})\s+([A-Z]*)\s+([0-9]\.[0-9]{2})\s+(?:(?:TBA|[MTWRFS]+)\s+(?:[0-9]{4}[AP]M)?-(?:[0-9]{4}[AP]M)?\s+(?:[A-Z\-]*)\s+(?:[0-9]+[A-Z]+|[A-Z]+[0-9]+|[0-9]+|\s+)\s*)+\n/g;
    var subCourseRegex = /(TBA|[MTWRFS]+)\s+([0-9]{4}[AP]M)?-([0-9]{4}[AP]M)?\s+([A-Z\-]*)\s+([0-9]+[A-Z]+|[A-Z]+[0-9]+|[0-9]+|\s+)\s*\s*/g
    var courseList = -1;

    this.createTestCourses = function() {
        courseList = new Array(0);

        /*Example courses. Will be filled from user input in the final version */
        list.push(new Course("FALL", "INTRO: CS FOR SCI,MATH&ENGR I", "CS -010 -001", "BRNHL", "A125", "None", 4,
                        9, 0, 10, 0, "MWF"));
        list.push(new Course("FALL", "INTRO: CS FOR SCI,MATH&ENGR I", "CS -010 -001", "BRNHL", "A125", "None", 4,
                        15, 30, 17, 0, "TR"));
    };

    this.createCourseList = function(rawString) {
        courseList = new Array(0);
        var quarter = /[0-9]{4} [A-z]+ Quarter/g.exec(rawString);
        quarter = /Fall|Winter|Spring|Summer/g.exec(quarter);
        var course = regex.exec(rawString);
        var hour1, min1, hour2, min2;

        //For each course
        while (course != null) {
            var subCourse = subCourseRegex.exec(course[0]);
            while(subCourse != null) {
                if (subCourse[2] != null) {
                    if (subCourse[2].substr(-2, 2).toUpperCase() == "AM") {
                        hour1 = parseInt(subCourse[2].substr(0, 2));
                    }
                    else {
                        hour1 = parseInt(subCourse[2].substr(0, 2)) + 12;
                    }

                    min1 = parseInt(subCourse[2].substr(2, 2));

                    if (subCourse[3].substr(-2, 2).toUpperCase() == "AM") {
                        hour2 = parseInt(subCourse[3].substr(0, 2));
                    }
                    else {
                        hour2 = parseInt(subCourse[3].substr(0, 2)) + 12;
                    }

                    min2 = parseInt(subCourse[3].substr(2, 2));

                    courseList.push(new Course(quarter, course[1], course[2], course[3], course[4],
                    subCourse[1], hour1, min1, hour2, min2, subCourse[4], subCourse[5]));
                }
                else {
                    $('.centered').append('<p>' + course[1] + " doesn't have a time. It's TBA.<br><p>");
                }
            subCourse = subCourseRegex.exec(course[0]);
            }

            course = regex.exec(rawString);
        }
    };
    this.getCourseList = function() {
        return courseList;
    }

    this.getRegex = function() {
        return regex;
    }
}
