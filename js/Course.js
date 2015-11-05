/**
 * Class to represent a course. Should be used in a list to represent a schedule.
 * Has functions avaliable to manipulate the data and present things in different ways.
 *
 * There are certain courses that do not have one period of time for one set of days.
 * These courses have multiple times for different days. (ex. One course but Tuesday class
 * meets at 7 where as Thrusday class meets at 8). These special cases are handeled by storing
 * them as two different courses. These two courses are technically one course but to represent
 * them better we have them as 2.
 *
 * @constructor
 * @author Bradley Cai
 */
function Course(quarter, name, nameID, gt, units,
                days, hour1, min1, hour2, min2, bldg, room) {

    //General information
    this.quarter = (quarter === "" ? "None provided" : quarter); //written as a string in the format of "season####"
    this.name = name;
    this.nameID = nameID; //ID written under the name of the course. (ex. CHEM-001A-060)
    this.bldg = (bldg === "" ? "TBA" : bldg); //String of the bldg
    this.room = (room === "" ? "TBA" : room); //String of room number
    this.gt = (gt === "" ? "None" : gt); //GT - Grade type. No one knows what this is
    this.units = units; //Expressed as a double

    //Time information
    this.hour1 = hour1; //Hour class begins. Integer between 1-24
    this.min1 = min1; //Minute class begins. Integer between 0-60
    this.hour2 = hour2; //Hour when class ends.
    this.min2 = min2;
    this.times = "";
    if (this.hour1 !== undefined || this.hour1 === "") {
        this.times =
            Math.ceil(this.hour1 % 12.1) + ":" + this.min1 + (this.min1 === 0 ? "0" : "") +
            (this.hour1 < 12 ? "am" : "pm") + " – " +
            Math.ceil(this.hour2 % 12.1) + ":" + this.min2 + (this.min2 === 0 ? "0" : "") +
            (this.hour2 < 12 ? "am" : "pm");
    }

    //Array information
    this.minDiff = this.min2 - this.min1;
    this.minBlock = 0;
    if (this.minDiff >= 15) {
        this.minBlock = 1;
    }
    else if (this.minDiff <= -15) {
        this.minBlock = -1;
    }
    this.blocks = 2 * (this.hour2 - this.hour1) + this.minBlock; //How many 30 minute blocks it takes (ex 60 is 2 blocks)
    this.duration = 30 * this.blocks; //Duration of class in minutes (ex. 60 for 60 minutes)
    this.pos = parseInt(((this.hour1 * 60 + this.min1) - 420) / 30); //Position on the hourList
    this.days = [false, false, false, false, false, false]; //Array of days as booleans.
    this.index = -1;
    if (days !== undefined) {
        for (var i = 0; i < days.length; i++) {
            switch (days.charAt(i)) {
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

    this.setIndex = function (index) {
        this.index = index;
    };
}
