function Course(quarter, name, nameID, gt, units, days, hour1, hour2, min1, min2, bldg, room) {
    this.quarter = quarter; //written as a string in the format of "season####"
    this.name = name;
    this.nameID = nameID; //ID written under the name of the course. (ex. CHEM-001A-060)
    this.gt = gt; //GT - Grade type. No one knows what this is. 
    this.units = units; //Expressed as a double
    this.days = days; //String of which days. You can use toDayList() as well. (ex. MWF)
    this.hour1 = hour1; //Hour class begins. Integer between 0-23
    this.hour2 = hour2; //Hour when class ends.
    this.min1 = min1; //Integer between 0-59
    this.min2 = min2; 
    this.bldg = bldg; //String of the bldg
    this.room = room; //String of room number
    
    /**
     * Turns the string of days from the schedule into a list of numbers.
     * 0 is Monday, 4 is Friday.
     *
     * @this {Course}
     * @return {dayList} list of days
     */
    this.toDayList = function() {
        dayList = [days.length()];
        for(i = 0; i < days.length(); i++) {
            day = days[i];
            switch(day) {
                case M:
                    dayList[i] = 0;
                case T:
                    dayList[i] = 1;
                case W:
                    dayList[i] = 2;
                case R:
                    dayList[i] = 3;
                case F:
                    dayList[i] = 4;
            }
        }
        return dayList;
    }
    
    //this.toFullBldg() = function() {} to be done later  
}