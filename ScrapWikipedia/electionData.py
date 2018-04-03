class Election:

    def __init__(self, name, year):
        self.name = name
        self.year = year
        self.districts = []

    def to_string(self):
        s = self.name
        s += ' ' + self.year
        s += '\nDistricts:\n'
        for district in self.districts:
            s += district.to_string() + '\n'
        return s

class District:
    def __init__(self, name):
        self.name = name
        self.winner = 0;
        self.candidates = []

    def setWinner(self):
        max = 0
        maxCandidate = 0
        for i in range(0, len(self.candidates)):
            candidate = self.candidates[i]
            if(candidate.percent > max):
                max = candidate.percent;
                maxCandidate = i;
        self.winner = maxCandidate;

    def getWinner(self):
        return self.candidates[self.winner]

    def to_string(self):
        s = 'District: ' + self.name
        s += '\nCandidates:\n'
        for i in range(0, len(self.candidates)):
            candidate = self.candidates[i]
            if(i == self.winner):
                s += candidate.to_string() + '\tWINNER\n'
            else:
                s += candidate.to_string() + '\n'
        return s

class Candidate:

    def __init__(self, name, party, percent):
        self.name = name
        if(party == 'D'):
            self.party = 'Democratic'
        elif(party == 'R'):
            self.party = 'Republican'
        elif(party == 'C'):
            self.party = 'Constitution'
        elif(party == 'L'):
            self.party = 'Libertarian'
        elif(party == 'G'):
            self.party = 'Green'
        elif(party == 'I'):
            self.party = 'Independent'
        else:
            self.party = party
        self.percent = percent

    def to_string(self):
        return self.name + '\t' + self.party + '\t' + str(self.percent)