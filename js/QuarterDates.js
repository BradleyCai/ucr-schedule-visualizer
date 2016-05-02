/**
 * Class to predict the starting dates of the fall, winter, and spring quarters.
 * Based on data from previous years, this class will use the JavaScript time library
 * to try to determine which days the quarter will start one. This class will always
 * return a Monday, regardless of the actual day classes begin.
 *
 * @constructor
 * @author Ammon Smith
 */
function QuarterDates(startYear, quarter) {
    //Refers to the first calendar year within one school year
    //So the 2015-2016 school year is represented by passing in '2015'
    //If the startYear passed in is empty(no year was given) then defaults to the current year
    this.startYear = (startYear === "" ? new Date().getFullYear() : parseInt(startYear));

    //Quarter of the course
    //If the quarter passed in is empty then default to Fall quarter
    this.quarter = (quarter === "" ? "Fall" : quarter);

    //List of unusual start dates that don't fit the normal pattern
    this.quirks = new Array(0);
    this.quirks["2014-fall"] = new Date(2014, 8, 29);

    //Class methods
    this.getFallStartDate = function () {
        var fallResult = this.quirks[this.startYear + "-fall"];
        if (fallResult !== undefined) {
            return fallResult;
        }

        //Second to last week of September, Thursday
        fallResult = new Date(this.startYear, 8, 23);
        fallResult.setDate(fallResult.getDate() - fallResult.getDay() + 4);
        return fallResult;
    };

    this.getFallEndDate = function() {
        var fallResult = this.getFallStartDate();

        // 10 weeks = 10 * 7 days
        fallResult.setDate(fallResult.getDate() + (9 * 7 + 6));
        return fallResult;
    };

    this.getWinterStartDate = function () {
        var winterResult = this.quirks[this.startYear + "-winter"];
        if (winterResult !== undefined) {
            return winterResult;
        }

        //Second week of January, Monday
        winterResult = new Date(this.startYear + 1, 0, 7);
        winterResult.setDate(winterResult.getDate() - winterResult.getDay() + 1);
        return winterResult;
    };

    this.getWinterEndDate = function() {
        var winterResult = this.getWinterStartDate();

        winterResult.setDate(winterResult.getDate() + (9 * 7 + 6));
        return winterResult;
    };

    this.getSpringStartDate = function () {
        var springResult = this.quirks[this.startYear + "-spring"];
        if (springResult !== undefined) {
            return springResult;
        }

        //Last week of March, Monday
        springResult = new Date(this.startYear + 1, 3, 0);
        springResult.setDate(springResult.getDate() - springResult.getDay() + 1);
        return springResult;
    };

    this.getSpringEndDate = function() {
        var springResult = this.getSpringStartDate();

        springResult.setDate(springResult.getDate() + (9 * 7 + 6));
        return springResult;
    };

    this.getQuarterStartDate = function() {
        switch (this.quarter) {
            case "Fall":
                return this.getFallStartDate();
            case "Winter":
                return this.getWinterStartDate();
            case "Spring":
                return this.getSpringStartDate();
            default:
                break;
        }
    };

    this.getQuarterEndDate = function() {
        switch (this.quarter) {
            case "Fall":
                return this.getFallEndDate();
            case "Winter":
                return this.getWinterEndDate();
            case "Spring":
                return this.getSpringEndDate();
            default:
                return;
        }
    };
}
