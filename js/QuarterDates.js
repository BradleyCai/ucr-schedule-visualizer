/**
 * Class to predict the starting dates of the fall, winter, and spring quarters.
 * Based on data from previous years, this class will use the JavaScript time library
 * to try to determine which days the quarter will start one. This class will always
 * return a Monday, regardless of the actual day classes begin.
 *
 * @constructor
 * @author Ammon Smith
 */
function QuarterDates(startYear) {
    //Refers to the first calendar year within one school year
    //So the 2015-2016 school year is represented by passing in '2015'
    this.startYear = startYear;
    
    //Cached results from class methods
    this.fallResult = undefined;
    this.winterResult = undefined;
    this.springResult = undefined;
    
    //List of unusual start dates that don't fit the normal pattern
    this.quirks = new Array();
    this.quirks["2014-fall"] = new Date(2014, 8, 29);

    //Class methods
    this.getFallStartDate = function () {
        if (this.fallResult !== undefined) {
            return this.fallResult;
        }

        this.fallResult = this.quirks[this.startYear + "-fall"];
        if (this.fallResult !== undefined) {
            return this.fallResult;
        }

        //Second to last week of September, Thursday
        this.fallResult = new Date(this.startYear, 8, 23);
        this.fallResult.setDate(this.fallResult.getDate() - this.fallResult.getDay() + 1);
        return this.fallResult;
    };

    this.getWinterStartDate = function () {
        if (this.winterResult !== undefined) {
            return this.winterResult;
        }

        this.winterResult = this.quirks[this.startYear + "-winter"];
        if (this.winterResult !== undefined) {
            return this.winterResult;
        }

        //Second week of January, Monday
        this.winterResult = new Date(this.startYear + 1, 0, 7);
        this.winterResult.setDate(this.winterResult.getDate() - this.winterResult.getDay() + 1);
        return this.winterResult;
    };

    this.getSpringStartDate = function () {
        if (this.springResult !== undefined) {
            return this.springResult;
        }

        this.springResult = this.quirks[this.startYear + "-spring"];
        if (this.springResult !== undefined) {
            return this.springResult;
        }

        //Last week of March, Monday
        this.springResult = new Date(this.startYear + 1, 3, 0);
        this.springResult.setDate(this.springResult.getDate() - this.springResult.getDay() + 1);
        return this.springResult;
    };
}

