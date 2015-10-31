var buildingNames = {
    "A&I"      : "Aberdeen_Inverness Residence Hall",
    "AHF"      : "Amy Harrison Field",
    "ALUM"     : "Alumni and Visitor Center",
    "ANDHL"    : "Anderson Hall 1 (AGSM)",
    "ANDU2"    : "Anderson Hall 2 (AGSM)",
    "ARTS"     : "Arts Building",
    "ATH"      : "Athletics and Dance Building",
    "BANNA"    : "Bannockburn Village A",
    "BANNB"    : "Bannockburn Village B",
    "BANNC"    : "Bannockburn Village C",
    "BANND"    : "Bannockburn Village D",
    "BANNE"    : "Bannockburn Village E",
    "BANNF"    : "Bannockburn Village F",
    "BANNG"    : "Bannockburn Village G",
    "BANNH"    : "Bannockburn Village H",
    "BANNI"    : "Bannockburn Village I",
    "BANNJ"    : "Bannockburn Village J",
    "BANNK"    : "Bannockburn Village K",
    "BANNL"    : "Bannockburn Village L",
    "BANNM"    : "Bannockburn Village M",
    "BANNN"    : "Bannockburn Village N",
    "BANNO"    : "Bannockburn Village O",
    "BANNP"    : "Bannockburn Village P",
    "BANNQ"    : "Bannockburn Village Q",
    "BANNQ"    : "Bannockburn Village Q",
    "BANNR"    : "Bannockburn Village R",
    "BANNS"    : "Bannockburn Village S",
    "BANNT"    : "Bannockburn Village T",
    "BANNU"    : "Bannockburn Village U",
    "BANNV"    : "Bannockburn Village V",
    "BARN"     : "The Barn",
    "BATCH"    : "Batchelor Hall",
    "BIOSC"    : "Biological Sciences",
    "BMSTC"    : "Biomedical Teaching Complex",
    "BOOKS"    : "Campus Bookstore",
    "BOTIC"    : "Botanic Gardens",
    "BOYDN"    : "Boyden Lab",
    "BOYHL"    : "Boyce Hall",
    "BRNHL"    : "Bourns Hall",
    "BTOWR"    : "Bell Tower",
    "CBN"      : "College Building North",
    "CBS"      : "College Building South",
    "CCCTR"    : "Computing and Communications",
    "CDEVC"    : "Child Development South",
    "CDEVCN"   : "Child Development North",
    "CDEVEADY" : "Eady Center",
    "CHEM"     : "Chemical Sciences",
    "CHPHL"    : "Chapman Hall",
    "CHUNG"    : "Winston Chung Hall",
    "COSTH"    : "Costo Hall",
    "EI&Q"     : "East I & Q (Insectary)",
    "ENTMU"    : "Entology Research Museum",
    "FAWLB"    : "Fawcett Lab",
    "FLKRK"    : "Falkirk Apartments",
    "GEOL"     : "Geology Building",
    "GHO2A"    : "Green House 2 A",
    "GMH1B"    : "Glen Mor 1 B",
    "GMH1D"    : "Glen Mor 1 D",
    "GMH1E"    : "Glen Mor 1 E",
    "HDHL"     : "Highlander Hall",
    "HERB"     : "Herbarium",
    "HINHL"    : "Administration (Hinderaker Hall)",
    "HMNSS"    : "Humanities and Social Sciences",
    "HSERV"    : "Veitch Student Center",
    "HUB"      : "Highlander Union Building (HUB)",
    "HUMN"     : "Humanities / University Theatre",
    "INTN"     : "CHASS Interdisciplinary North",
    "INTS"     : "CHASS Interdisciplinary South",
    "INTVLW"   : "International Village - Apartments West Wing",
    "KUCR"     : "KUCR Radio",
    "L55H"     : "Latitude 55 (HUB)",
    "LFSC"     : "Life Sciences",
    "LOTH"     : "Lothian Residence Hall",
    "MSE"      : "Material Science & Engineering",
    "OBAN"     : "Oban Apartments",
    "OBANA"    : "Oban Apartments A",
    "OBANB"    : "Oban Apartments B",
    "OBANC"    : "Oban Apartments C",
    "OBAND"    : "Oban Apartments D",
    "OBANE"    : "Oban Apartments E",
    "OBANF"    : "Oban Apartments F",
    "OBANG"    : "Oban Apartments G",
    "OBANH"    : "Oban Apartments H",
    "OBANI"    : "Oban Apartments I",
    "OBANJ"    : "Oban Apartments J",
    "OLMH"     : "Olmsted Hall",
    "ORBLI"    : "Orbach Science Library",
    "P1"       : "Parking P1",
    "P11"      : "Parking P11",
    "P13"      : "Parking P13",
    "P14"      : "Parking P14",
    "P15"      : "Parking P15",
    "P19"      : "Parking P19",
    "P20"      : "Parking P20",
    "P22"      : "Parking P22",
    "P24"      : "Parking P24",
    "P26"      : "Parking P26",
    "P4"       : "Parking P4",
    "P41"      : "Parking P41",
    "P5"       : "Parking P5",
    "P6"       : "Parking P6/V6",
    "PARKS"    : "Parking Services",
    "PENTA"    : "Pentland Hills - Building A",
    "PENTB"    : "Pentland Hills - Building B",
    "PENTC"    : "Pentland Hills - Building C",
    "PENTD"    : "Pentland Hills - Building D",
    "PENTE"    : "Pentland Hills - Building E",
    "PENTF"    : "Pentland Hills - Building F",
    "PENTG"    : "Pentland Hills - Building G",
    "PENTH"    : "Pentland Hills - Building H",
    "PENTI"    : "Pentland Hills - Building I",
    "PENTJ"    : "Pentland Hills - Building J",
    "PENTK"    : "Pentland Hills - Building K",
    "PENTL"    : "Pentland Hills - Building L",
    "PENTM"    : "Pentland Hills - Building M",
    "PENTN"    : "Pentland Hills - Building N",
    "PENTO"    : "Pentland Hills - Building O",
    "PENTP"    : "Pentland Hills - Building P",
    "PENTQ"    : "Pentland Hills - Building Q",
    "PHY"      : "Physics Building",
    "POLCE"    : "Police Facility",
    "PR"       : "Printing and Reprographics",
    "PRCE"     : "Pierce Hall",
    "PRSNL"    : "Human Resources",
    "PSYCH"    : "Psychology Building",
    "RIVL"     : "Rivera Library",
    "SCLAB"    : "Science Laboratories 1",
    "SOCS"     : "UCR Soccer Stadium",
    "SOMR"     : "School of Medicine Research Building",
    "SPR"      : "Sproul Hall",
    "SPTCN"    : "UC Riverside Baseball Complex",
    "SPTH"     : "Spieth Hall",
    "SRCTC"    : "UCR Student Recreation Center Tennis Courts",
    "SSB"      : "Student Services",
    "STAT"     : "School of Medicine Education Building",
    "STREC"    : "Student Recreation Center",
    "SURGE"    : "Campus Surge",
    "UCREX"    : "UCR Extension Center",
    "UNLH"     : "University Lecture Hall",
    "UOB"      : "University Office Building",
    "UP"       : "University Plaza Apartments",
    "UV"       : "University Village",
    "WAT"      : "Watkins Hall",
    "WEBHL"    : "Webber Hall",
    "X8"       : "UC Riverside Track and Field Stadium",
    "XSTA"     : "Arts 113-Studio Theatre",
    "XWRH"     : "Watkins Hall 1000",
};


/**
 * Class to represent a course. Should be used in a list to represent a schedule.
 * Has functions avaliable to manipulate the data and present things in different ways.
 * 
 * @constructor 
 * @author Bradley Cai
 */
function Course(quarter, name, nameID, bldg, room, gt, units,
                hour1, min1, hour2, min2, days) {
    
    //General information
    this.quarter = quarter; //written as a string in the format of "season####"
    this.name = name;
    this.nameID = nameID; //ID written under the name of the course. (ex. CHEM-001A-060)
    this.bldg = bldg; //String of the bldg
    this.room = room; //String of room number
    this.gt = gt; //GT - Grade type. No one knows what this is
    this.units = units; //Expressed as a double
    
    //Time information
    this.hour1 = hour1; //Hour class begins. Integer between 0-23
    this.min1 = min1; //Minute class begins. Integer between 0-59
    this.hour2 = hour2; //Hour when class ends.
    this.min2 = min2;
    if (hour1 != null) {
        this.times = Math.ceil(hour1%12.1) + ":" +(min1 + 10) + ((hour1 < 12) ? "am" : "pm") + " – " 
        + Math.ceil(hour2%12.1) + ":" + (min2 + 10) + ((hour2 < 12) ? "am" : "pm");
    }
    
    //Array information
    this.blocks = 2*(this.hour2 - this.hour1) - (this.min2 - this.min1)/30; //How many 30 minute blocks it takes (ex 60 is 2 blocks)
    this.duration = 30 * this.blocks; //Duration of class in minutes (ex. 60 for 60 minutes)
    this.pos = ((this.hour1 * 60 + this.min1) - 420)/30; //Position on the hourList
    this.days = [false, false, false, false, false, false]; //Array of days as booleans.
    this.index = -1;
    
    for(var i = 0; i < days.length; i++) {
        switch(days.charAt(i)) {
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
    
    this.setIndex = function(index) {
        this.index = index;
    }
}

/**
 * Test function to fill an array with dummy courses.
 *
 * @return - A fake courseList of courses. 
 */
function createTestCourses() {
    
    var list = new Array();
    
    /*Example courses. Will be filled from user input in the final version */
    list.push(new Course("FALL", "INTRO: CS FOR SCI,MATH&ENGR I", "CS -010 -001", "BRNHL", "A125", "None", 4,
                    9, 0, 10, 0, "MWF"));
    list.push(new Course("FALL", "GENERAL CHEMISTRY", "CHEM-001A-060", "INTN", "1020", "None", 4,
                    15, 30, 17, 0, "TR"));
    
    return list;
}

/**
 * Creates a 2D array whose rows are time in 30 minute blocks and columns days of the week.
 * The spot on a calender where the courses takes place in time on a certain day will fill
 * that postion on the array.
 * 
 * @param cList - A list of courses
 * @return hList - A 2D array hour list
 */
function createHourList(cList) {
    var hList;
    
    //Initialize a 2-D array. Each item within the array is an array.
    hList = new Array(32)
    for (var i = 0; i < 32; i++) {
        hList[i] = new Array(6);
    }
    
    for (var c = 0; c < cList.length; c++) { //for each course
        var current = cList[c];
        current.setIndex(c);
        for (var day = 0; day < current.days.length; day++) { //for each day of the week
            if (current.days[day] == true) {
                //console.log(cList[c].pos + " " + day);
                for (var b = 0; b < current.blocks; b++) {//for each block
                    hList[current.pos + b][day] = cList[c];
                }
            }
        }
    }
    
    return hList;
}

function drawCanvasTable(hList, canvas, width, height) {
    var offset = 100; //Sets the table down (offset) amount of pixels. Used for the title
    var tableWidth = width * hList[0].length + width + 1;
    var tableHeight = height * hList.length + height + 1 + offset;

    canvas.width = tableWidth;
    canvas.height = tableHeight;
    
    var context = canvas.getContext("2d");
    context.font = 'bold 50px "Helvetica"';
    context.textBaseline = "middle";
    context.textAlign = "center";
    
    var courseAtI;
    
    var days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    context.fillStyle="white";
    context.fillRect(0, 0, tableWidth, tableHeight);
    context.fillStyle="black";
    context.fillText("UCR Schedule Visualizer", tableWidth/2, 30);
    context.font = '18px "Helvetica"';
    context.fillText("https://waa.ai/ucrsv", tableWidth/2, 65);
    context.font = '14px "Helvetica"';
    
    for (var day = 0; day < days.length; day++) { //Heh, courses for days. No? Okay ;_;
        context.rect(day * width + width + .5, offset + .5, width, height);
        context.fillText(days[day], day*width + width + width/2, height/2 + offset); 
    }
    context.rect(.5, offset + .5, width, height);    
    
    var hour = 0;
    for (var row = 1; row < hList.length + 1; row++) { //For each 30 minute block
        if (row%2 == 1) {
            hour = Math.ceil(((row * 30 + 420)/60) % 12.1);
            context.rect(.5 ,row * height + offset + .5, width, height*2);
            if (Math.floor(row/10) == 0) {
                context.fillText(hour + "AM", .5 + width / 2, row * height + height + offset + .5); }
            else {
                context.fillText(hour + "PM", .5 + width / 2, row * height + height + offset + .5); }
            
        }
        
        for (var col = 1; col < hList[0].length + 1; col++) { //For each day Mon-Sat
            courseAtI = hList[row - 1][col - 1];
            
            if (courseAtI != null) {
                if (hList[row - 2][col - 1] == null) {
                    switch (courseAtI.blocks) {
                        case 1:
                            context.rect(col * width + .5, row * height + .5 + offset, width, height);
                            context.fillText(courseAtI.nameID, col*width + width/2, row*height + height/2 + offset);
                            break;
                        case 2:
                            context.fillStyle="#E6E6E6";
                            context.fillRect(col * width + .5, row * height + .5 + offset, width, height * 2);
                            context.fillStyle="black";
                            //context.fillStyle="black";
                            context.fillText(courseAtI.nameID, col*width + width/2, row*height + height/2 + offset);
                            context.fillText(courseAtI.bldg + " " + courseAtI.room, col*width + width/2, row*height + height + height/2 + offset);
                            break;
                        default:
                            context.fillStyle="#E6E6E6";
                            context.fillRect(col * width + .5, row * height + .5 + offset, width, height * courseAtI.blocks);
                            context.fillStyle="black";
                            context.fillText(courseAtI.nameID, col*width + width/2, row*height + height*courseAtI.blocks/2 - height + offset);
                            context.fillText(courseAtI.duration + " minutes", col*width + width/2, row*height + height*courseAtI.blocks/2 + offset);
                            context.fillText(courseAtI.bldg + " " + courseAtI.room, col*width + width/2, row*height + height*courseAtI.blocks/2 + height + offset);
                            break;
                    }
                }
            }
            else {
                context.rect(col * width + .5, row * height + .5 + offset, width, height);
            }
        }
    }
    
    context.stroke();
}

/**
 * Creates a string for the innerHTML element of the table. You can view the html in the console log
 * 
 * More is explained inside.
 *
 * @param hList - Hour list, get it from createHourList(cList)
 * @param cList - List of courses, gotten from the regex parsing
 */
function createTableString(hList) {
    //This creates the first row of days
    var tableString = 
"<table class='pure-table'>\n \
    <thead>\n \
        <tr>\n \
            <th></th>\n \
            <th>Monday</th>\n \
            <th>Tuesday</th>\n \
            <th>Wednesday</th>\n \
            <th>Thursday</th>\n \
            <th>Friday</th>\n \
            <th>Saturday</th>\n \
        </tr>\n \
    </thead>\n \
    <tbody>\n";
    
    //This creates the body of the table
    var hour = 0;
    for (var row = 0; row < 32; row++) { //for each tr/row (700 730 800 etc). 32 is the amount of rows. See blocks
        
        //Starts off the row with an hour ID to keep things readable
        tableString += "<tr id = '" + (row * 30 + 420)/60 + "'>\n";
        
        //This is the 12 hour clock mechanism
        hour = Math.ceil(((row * 30 + 420)/60) % 12.1);
        
        //This creates the first column of times and adds AM or PM based on time of day
        if (row % 2 == 0) { //To make each rowspan 2 time column
            if (Math.floor(row/10) == 0) {
                tableString += "<td rowspan='2'><strong>" + hour + "AM</strong></td>\n"; }
            else {
                tableString += "<td rowspan='2'><strong>" + hour + "PM</strong></td>\n"; }
        }
        
        //This creates the courses in the table
        for (var col = 0; col < 6; col++) { // for each td/day (mon - sat = 6)
            courseAtI = hList[row][col];
            
            //This displays the course info per course, instead of per block
            if (courseAtI != null) {
                if (hList[row - 1][col] == null) {
                    
                    var popoutString = "<td class='rspan' rowspan='" + courseAtI.blocks + "'>" +
                    "<a href='' onclick='return false;' " +
                    "class='course" + courseAtI.index + "'>\n";
                    
                    switch (courseAtI.blocks) {
                        case 1:
                            tableString += popoutString + courseAtI.nameID + "</a></td>\n";
                            break;
                        case 2:
                            tableString += popoutString + courseAtI.nameID + 
                            "<br>" + courseAtI.bldg + " " + courseAtI.room + "</a></td>\n";
                            break;
                        default:
                            tableString += popoutString + courseAtI.nameID + "<br>" + courseAtI.duration + " minutes<br>" + 
                            courseAtI.bldg + " " + courseAtI.room + "</a></td>\n"
                            break;
                    }
                    
                }
            }
            else {
                tableString += "<td></td>\n";
            }
        }
    }
    tableString += "</thead>\n</table>";
    return tableString;
}

/**
 * This will find the div with an ID of "table-space" and then insert the innerHTML that createTableString() made.
 * Will also display the tableString on the console log
 *
 */
function createTable(tableString) {
    var tableSpace = document.getElementById("table-space");
    console.log(tableString);
    
    tableSpace.innerHTML = tableString;
    
    console.log(tableString);
}

function createPopovers(cList) {
    for (var c = 0; c < cList.length; c++) {
        courseAtI = cList[c];
        console.log(courseAtI.bldg);
        
        //This block will give "None" to empty variables in a course
        var gt = (courseAtI.gt == "") ? "None" : courseAtI.gt;
        var times = (courseAtI.hour1 == "") ? "None" : courseAtI.times;
        var days = (courseAtI.days == "") ? "None" : courseAtI.days;
        var bldg = (courseAtI.bldg == "") ? "None" : courseAtI.bldg;
        var room = (courseAtI.room == "") ? "None" : courseAtI.room;
        var locat = getBuildingLocation(bldg, room);
        
        $('.course' + c).popover({title: courseAtI.name, 
        content: "<strong>Times: </strong>" + times + 
        " <br><strong>Building:</strong> " + bldg + 
        " <br><strong>Room:</strong> " + room + 
        " <br><strong>GT:</strong> " + gt +
        " <br><strong>Location:</strong> " + locat,
        html: true, 
        animation: true, 
        trigger: "focus"}); 
    }
}

function getBuildingLocation(bldg, room) {
    name = buildingNames[bldg];
    url = "http://campusmap.ucr.edu/imap/index.html?loc=" + bldg;

    if (name == undefined || name == "undefined")
        return "Unknown";

    return "<a href=\"" + url + "\">" + name + " " + room + "</a>";
}

/**
 * Creates all of the parts related to this website. Makes the hourList then the tableString
 * and then the actual table and then fills it with popovers
 *
 * @param courseList - List of courses, see Course class
 */
function createAll(courseList) {
    var hourList;
    var tableString;
    var canvas;

    hourList = createHourList(courseList);
    tableString = createTableString(hourList);
    canvas = document.createElement('canvas');
    
    createTable(tableString);
    createPopovers(courseList);
    drawCanvasTable(hourList, canvas, 150, 25);
    
    $(".btn").click(function() {
        canvas.toBlob(function(blob) {
            saveAs(blob, "UCR-Schedule-Visualized.png");
        });
    });
}

createAll(createTestCourses());
