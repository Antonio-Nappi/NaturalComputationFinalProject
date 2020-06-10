#In this script there are two classes those are used from client

class Track():
    def __init__(self):
        self.laplength = 0
        self.width = 0
        self.sectionList = list()
        self.usable_model = False

    def __repr__(self):
        o = 'TrackList:\n'
        o += '\n'.join([repr(x) for x in self.sectionList])
        o += "\nLap Length: %s\n" % self.laplength
        return o

    def post_process_track(self):
        ws = [round(s.width) for s in self.sectionList]
        ws = [O for O in ws if O]
        ws.sort()
        self.width = ws[len(ws) / 2]
        cleanedlist = list()
        TooShortToBeASect = 6
        for n, s in enumerate(self.sectionList):
            if s.dist > TooShortToBeASect:
                if cleanedlist and not s.direction and not cleanedlist[-1].direction:
                    cleanedlist[-1].end = s.end
                else:
                    cleanedlist.append(s)
            else:
                if cleanedlist:
                    prevS = cleanedlist[-1]
                    prevS.end = s.apex
                    prevS.dist = prevS.end - prevS.start
                    prevS.apex = prevS.dist / 2 + prevS.start
                if len(self.sectionList) - 1 >= n + 1:
                    nextS = self.sectionList[n + 1]
                    nextS.start = s.apex
                    nextS.dist = nextS.end - nextS.start
                    nextS.apex = nextS.dist / 2 + nextS.start
                else:
                    prevS.end = T.laplength
                    prevS.dist = prevS.end - prevS.start
                    prevS.apex = prevS.dist / 2 + prevS.start
        self.sectionList = cleanedlist
        self.usable_model = True

    def write_track(self, fn):
        firstline = "%f\n" % self.width
        f = open(fn + '.trackinfo', 'w')
        f.write(firstline)
        for s in self.sectionList:
            ts = '%f %f %f %d\n' % (s.start, s.end, s.magnitude, s.badness)
            f.write(ts)
        f.close()

    def load_track(self, fn):
        self.sectionList = list()
        with open(fn + '.trackinfo', 'r') as f:
            self.width = float(f.readline().strip())
            for l in f:
                data = l.strip().split(' ')
                TS = TrackSection(float(data[0]), float(data[1]), float(data[2]), self.width, int(data[3]))
                self.sectionList.append(TS)
        self.laplength = self.sectionList[-1].end
        self.usable_model = True

    def section_in_now(self, d):
        for s in self.sectionList:
            if s.start < d < s.end:
                return s
        else:
            return None

    def section_ahead(self, d):
        for n, s in enumerate(self.sectionList):
            if s.start < d < s.end:
                if n < len(self.sectionList) - 1:
                    return self.sectionList[n + 1]
                else:
                    return self.sectionList[0]
        else:
            return None

    def record_badness(self, b, d):
        sn = self.section_in_now(d)
        if sn:
            sn.badness += b


class TrackSection():
    def __init__(self, sBegin, sEnd, sMag, sWidth, sBadness):
        if sMag:
            self.direction = int(abs(sMag) / sMag)
        else:
            self.direction = 0
        self.start = sBegin
        self.end = sEnd
        self.dist = self.end - self.start
        if not self.dist: self.dist = .1
        self.apex = self.start + self.dist / 2
        self.magnitude = sMag
        self.width = sWidth
        self.severity = self.magnitude / self.dist
        self.badness = sBadness

    def __repr__(self):
        tt = ['Right', 'Straight', 'Left'][self.direction + 1]
        o = "S: %f  " % self.start
        o += "E: %f  " % self.end
        o += "L: %f  " % (self.end - self.start)
        o += "Type: %s  " % tt
        o += "M: %f " % self.magnitude
        o += "B: %f " % self.badness
        return o

    def update(self, distFromStart, trackPos, steer, angle, z):
        pass

    def current_section(self, x):
        return self.begin <= x and x <= self.end