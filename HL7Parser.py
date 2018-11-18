


# Function to read in HL7 text file
def openFile(file):
    with open (file, "r") as f:
        for i, line in enumerate(f):
            print("Line %s %s"% (i, line))

# Function to parse HL7 data into fields
def parseFields(file):
    with open (file, "r") as f:
        for i, line in enumerate(f):
            fieldlist = line.split("|")
            for i, field in enumerate(fieldlist):
                print("%s Field %s: %s"%(fieldlist[0], i, field))

# Function to parse HL7 data into components
def parseComponents(file):
    with open (file, "r") as f:
        for i, line in enumerate(f):
            fields = line.split("|")
            for i, fields in enumerate(fields):
                compsList = fields.split("^")
                for i, comps in enumerate(compsList):
                    print("%s Component %s: %s"%(compsList[0], i, comps))

# Function to parse HL7 data into subcomponents

def parseSubcomponents (file):
    with open(file, 'r') as f:
        for c, line in enumerate (f):
            print ("Segment {}:".format(c))
            for c, fld in enumerate (line.split('|')):
                print ("     Field {}:".format(c))
                if (fld == "^~\&"):
                    print("          SubComponent{}: {}".format(0, fld))
                else:
                    for c, comp in enumerate (fld.split('^')):
                        print("          Component{}:".format(c))
                        for c, subcomp in enumerate (comp.split('~')):
                            print("SubComponent{}: {}".format(c, subcomp))

# Function to parse HL7 data into JSON formatted structure

def convertToJSON(file):
    with open (file, 'r') as f:
        file = f.read()
        msgList = file.split('\r\n')
        messages = {}
        for cnt0, msg in enumerate(msgList, 1):
            segmentList = msg.split('\n')
            segments = {}
            segmentTracker = {}
            msgK = 'MSG %s' % cnt0
            for cnt1, seg in enumerate(segmentList, start=1):
                fieldsList = seg.split('|')
                fields = {}
                if (seg == ''):
                    continue
                else:
                    for cnt2, fld in enumerate(fieldsList, start=1):
                        flak = 'FLD %s' % cnt2
                        if (fld == ''):
                            continue
                        elif ((fld == '^~\&') or (fld == '^~`&') or (len(fld.split('^'))==1)):
                            fields[flak] = fld
                        else:
                            componentList = fld.split('^')
                            comps = {} 
                            for cnt3, cmp in enumerate(componentList, start=1):
                                subcomponentList = cmp.split('~')
                                subComps = {}
                                compsK = 'CMP %s' % cnt3
                                if (cmp == ''):
                                    continue
                                elif (len(subcomponentList)==1):
                                    comps[compsK] = cmp
                                else:
                                    for cnt4, sc in enumerate(subcomponentList, start=1):
                                        subCompsK = 'SCMP %s' % cnt4
                                        if (sc == ''):
                                            continue
                                        else:
                                            subComps[subCompsK] = sc
                                    comps[compsK] = subComps
                            fields[flak] = comps
                if (fieldsList[0] not in segmentTracker):
                    segmentTracker[fieldsList[0]] = 1
                else:
                    n = segmentTracker[fieldsList[0]] +1
                    segmentTracker[fieldsList[0]] = n
                segK = '%s %s' % (fieldsList[0], segmentTracker[fieldsList[0]])
                segments[segK] = fields
            messages[msgK] = segments
        print(messages)

