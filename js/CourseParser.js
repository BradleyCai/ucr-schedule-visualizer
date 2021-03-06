function CourseParser() {
    // CourseParser.regex is in charge of finding each course
    this.regex = /(.*)\n\s*([A-Z]+ ?-[A-Z0-9]+ ?-[A-Z0-9]+)\s+([A-Z]*)\s+([0-9]\.[0-9]{2})\s+((?:\s*(?:TBA|[MTWRFS]{1,6})\s+(?:[0-9]{4}[AP]M)?-(?:[0-9]{4}[AP]M)?\s*(?:(?!^)[A-Z\-]{0,8}|ONLINE)\s*(?:(?!^)([A-Z]*[0-9]*[A-Z]*)|COURSE)?\s*$)+)/gm;

    // CourseParser.subCourseRegex is in charge of extracting the times and locations of the course
    this.subCourseRegex = /(TBA|[MTWRFS]+)\s*([0-9]{4}[AP]M)-([0-9]{4}[AP]M)\s*([A-Z\-]{0,8}|ONLINE)\s*([0-9]+[A-Z]+|[A-Z]+[0-9]+|[0-9]+|COURSE)?\s*\n/gm;

    // CourseParser.courseList holds the displayed courses, CourseParser.noShowList holds the courses that are not displayed.
    this.courseList = -1;
    this.noShowList = -1;

    this.createCourseList = function (rawString) {
        this.courseList = new Array(0);
        this.noShowList = new Array(0);
        var quarter = /[0-9]{4} [A-z]+ Quarter/g.exec(rawString);
        var year;
        var course = this.regex.exec(rawString);
        var hour1, min1, hour2, min2;

        if (quarter !== null) {
            year = parseInt(/[0-9]{4}/g.exec(rawString)[0]);
            quarter = /Fall|Winter|Spring|Summer/g.exec(quarter)[0];
        }
        else {
            quarter = "";
            year = "";
        }

        //For each course
        while (course !== null) {
            var subCourse = this.subCourseRegex.exec(course[5]);
            while (subCourse !== null) {
                if (subCourse[2] !== undefined) {
                    if (subCourse[2].substr(-2, 2).toUpperCase() == "AM") {
                        hour1 = parseInt(subCourse[2].substr(0, 2)) % 12;
                    }
                    else {
                        hour1 = parseInt(subCourse[2].substr(0, 2)) % 12 + 12;
                    }

                    min1 = parseInt(subCourse[2].substr(2, 2));

                    if (subCourse[3].substr(-2, 2).toUpperCase() == "AM") {
                        hour2 = parseInt(subCourse[3].substr(0, 2)) % 12;
                    }
                    else {
                        hour2 = parseInt(subCourse[3].substr(0, 2)) % 12 + 12;
                    }

                    min2 = parseInt(subCourse[3].substr(2, 2));

                    if (7 < hour1 && hour1 < 22 && 7 < hour2 && hour2 < 22) {
                        this.courseList.push(new Course(quarter, year, course[1], course[2], course[3], course[4],
                        subCourse[1], hour1, min1, hour2, min2, subCourse[4], subCourse[5]));
                    }
                    else {
                        var unrecognizedString = '<div class="container" id ="unrecognized"><p class = "alert alert-error"><strong>Something went wrong!</strong> Your schedule refers to a time that is out of range! We didn\'t expect any classes after 10PM or before 7AM. Send us an email and we\'ll figure something out.';
                        $(".table-space").before(unrecognizedString);
                    }
                }
                else {
                    this.noShowList.push(new Course(quarter, year, course[1], course[2], course[3], course[4],
                        subCourse[1], hour1, min1, hour2, min2, subCourse[4], subCourse[5]));
                }
                subCourse = this.subCourseRegex.exec(course[5]);
            }
            course = this.regex.exec(rawString);
        }

        // For each course that won't show up
        if (this.noShowList.length > 0) {
            var noShowString = '<div class="container" id = "noShow"><p class = "alert alert-error"><strong>One or more classes are not shown because their times are either TBA or missing: </strong><br><br>';
            for (var i = 0; i < this.noShowList.length; i++) {
                noShowString += this.noShowList[i].name + " (" + this.noShowList[i].nameID + ")" + "<br>";
            }
            noShowString += "</a></div>";

            $(".table-space").before(noShowString);
        }
        if (quarter === "" || year === 0) {
            var noYearInfoAlert = '<div class="container" id = "noShow"><p class = "alert alert-error"><strong> Quarter and year are missing </strong><br><br> We didn\'t see the quarter or the year in the schedule you gave us! Next time copy the whole thing. </p></div>';

            $(".table-space").before(noYearInfoAlert);
        }
    };

    this.getCourseList = function () {
        return this.courseList;
    };

    this.getRegex = function () {
        return this.regex;
    };
}