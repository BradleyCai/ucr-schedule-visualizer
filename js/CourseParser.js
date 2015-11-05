function CourseParser() {
    this.regex = /(.*)\n\s*([A-Z]+ ?-[A-Z0-9]+ ?-[0-9]{3})\s+([A-Z]*)\s+([0-9]\.[0-9]{2})\s+(?:\s*(?:TBA|[MTWRFS]{1,6})\s+(?:[0-9]{4}[AP]M)?-(?:[0-9]{4}[AP]M)?\s*(?:[A-Z\-]{0,8})\s*(?:[0-9]+[A-Z]{1}|[A-Z]{1}[0-9]+|[0-9]+|\s+)\s*\n)+/g;
    this.subCourseRegex = /(TBA|[MTWRFS]+)\s*([0-9]{4}[AP]M)?-([0-9]{4}[AP]M)?\s*([A-Z\-]{0,8})\s*([0-9]+[A-Z]+|[A-Z]+[0-9]+|[0-9]+|\s*)\n/g;
    this.courseList = -1;
    this.noShowList = -1;

    this.createTestCourses = function () {
        courseList = new Array(0);

        /*Example courses. Will be filled from user input in the final version */
        list.push(new Course("FALL", "INTRO: CS FOR SCI,MATH&ENGR I", "CS -010 -001", "BRNHL", "A125", "None", 4,
            9, 0, 10, 0, "MWF"));
        list.push(new Course("FALL", "INTRO: CS FOR SCI,MATH&ENGR I", "CS -010 -001", "BRNHL", "A125", "None", 4,
            15, 30, 17, 0, "TR"));
    };

    this.createCourseList = function (rawString) {
        this.courseList = new Array(0);
        this.noShowList = new Array(0);
        var quarter = /[0-9]{4} [A-z]+ Quarter/g.exec(rawString);
        var course = this.regex.exec(rawString);
        var hour1, min1, hour2, min2;

        if (quarter !== null) {
            quarter = /Fall|Winter|Spring|Summer/g.exec(quarter)[1];
        }
        else {
            quarter = "";
        }

        //For each course
        while (course !== null) {
            var subCourse = this.subCourseRegex.exec(course[0]);
            while (subCourse !== null) {
                if (subCourse[2] != null) { // short hand for: if (typeof courseAtI !== 'undefined' && courseAtI !== null).
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

                    this.courseList.push(new Course(quarter, course[1], course[2], course[3], course[4],
                        subCourse[1], hour1, min1, hour2, min2, subCourse[4], subCourse[5]));
                }
                else {
                    this.noShowList.push(new Course(quarter, course[1], course[2], course[3], course[4],
                        subCourse[1], hour1, min1, hour2, min2, subCourse[4], subCourse[5]));
                }
                subCourse = this.subCourseRegex.exec(course[0]);
            }
            course = this.regex.exec(rawString);
        }

        // For each course that won't show up
        if (this.noShowList.length > 0) {
            var noShowString = '<div class="container"><p class = "alert alert-error"><strong>One or more classes are not shown because their times are either TBA or missing: </strong><br><br>';
            for (var i = 0; i < this.noShowList.length; i++) {
                noShowString += this.noShowList[i].name + " (" + this.noShowList[i].nameID + ")" + "<br>";
            }
            noShowString += "</a></div>";

            $(".centered").append(noShowString);
        }
    };
    this.getCourseList = function () {
        return this.courseList;
    };

    this.getRegex = function () {
        return this.regex;
    };
}
