/**
 * Class to represent a course. Should be used in a list to represent a schedule.
 * Has functions avaliable to manipulate the data and present things in different ways.
 * 
 * @constructor 
 * @author Bradley Cai
 */
function Course(quarter, name, nameId, gt, units, days, hour1, hour2, min1, min2, bldg, room) {
    this.quarter = quarter; //written as a string in the format of "season####"
    this.name = name;
    this.nameId = nameId; //ID written under the name of the course. (ex. CHEM-001A-060)
    this.gt = gt; //GT - Grade type. No one knows what this is. 
    this.units = units; //Expressed as a double
    this.days = [false, false, false, false, false, false]; //Array of days as booleans.
    this.hour1 = hour1; //Hour class begins. Integer between 0-23
    this.hour2 = hour2; //Hour when class ends.
    this.min1 = min1; //Integer between 0-59
    this.min2 = min2; 
    this.bldg = bldg; //String of the bldg
    this.room = room; //String of room number

    for(var i = 0; i < days.length(); i++) {
        switch(days.charAt(i)) {
            case 'M':
                this.days[0] = true;
                break;
            case 'T':
                this.days[1] = true;
                break;
            case 'W':
                this.days[2] = true;
                break;
            case 'R':
                this.days[3] = true;
                break;
            case 'F':
                this.days[4] = true;
                break;
            case 'S':
                this.days[5] = true;
        }
    }
}
