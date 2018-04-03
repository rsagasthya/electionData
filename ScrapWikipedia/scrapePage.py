import urllib.request
from bs4 import BeautifulSoup
import re
import electionData as e

def convertToInt(value_str):
    elements = value_str.split(',')
    value = 0
    for element in elements:
        value = (value*1000) + int(element)
    return value

def setName(name):
    elems = name.split(',')
    if('election' in elems[0]):
        return elems[0][:(-1*len('elections'))]
    return elems[0]

def getStateName(state):
    if(not '_' in state):
        return state
    elems = state.split('_')
    stateName = elems[0]
    for i in range(1, len(elems)):
        stateName += ' ' + elems[i]
    return stateName

def getAsCandidate(candidateStr):
    if('Write-ins' in candidateStr):
        elems = candidateStr.split(' ')
        name = elems[0]
        percentElems = re.split('%', elems[1].strip())
        percent = percentElems[0]
        party = 'I'
        candidate = e.Candidate(name, party, float(percent))
        return candidate

    elems = re.split('\\(', candidateStr)
    name = elems[0].strip()
    if(not all(ord(char) < 128 for char in name)):
        name = name[2:]
    addElems = re.split('\\)', elems[1].strip())
    party = addElems[0]
    percent = ''
    if ('unopposed' in addElems[1].lower()):
        percent = '100.0'
    else:
        percentElems = re.split('%', addElems[1].strip())
        percent = percentElems[0]
    candidate = e.Candidate(name, party, float(percent))
    return candidate

def get_election_data(state, yearStr):
    districts = []
    quote_page = 'https://en.wikipedia.org/wiki/United_States_House_of_Representatives_elections,_' + yearStr
    with urllib.request.urlopen(quote_page) as url:
        page = url.read()

    soup = BeautifulSoup(page, 'html.parser')
    title = soup.find('span', attrs={'id': state})

    tables = soup.find_all('table', attrs={'class': 'wikitable' or 'wikitable sortable jquery-tablesorter'})
    for table in tables:
        if(getStateName(state) in table.get_text() and ('Candidates' in table.get_text() or 'Opponent' in table.get_text())):
            rows = table.find_all('tr')
            for i in range(0, len(rows)):
                if('district' in rows[i].get_text().lower()):
                    continue
                if ('location' in rows[i].get_text().lower()):
                    continue
                if ('candidates' in rows[i].get_text().lower()):
                    continue
                attributes = rows[i].find_all('th')
                district_name = ''
                if(len(attributes) > 0):
                    district_name = attributes[0].get_text().strip()
                else:
                    attributes = rows[i].find_all('td')
                    district_name = attributes[0].get_text().strip()

                district = e.District(district_name)

                attributes = rows[i].find_all('td')
                if('unopposed' in attributes[len(attributes)-1].get_text().lower()):
                    candidate = attributes[len(attributes)-1].get_text().strip().split('\n')[0] + ' 100.00'
                    candidateObj = getAsCandidate(candidate)
                    district.candidates.append(candidateObj)
                else:
                    candidates = attributes[len(attributes)-1].get_text().strip().split('\n')
                    for candidate in candidates:
                        candidateObj =  getAsCandidate(candidate)
                        district.candidates.append(candidateObj)
                district.setWinner()
                districts.append(district)
    return districts

elections = []
states = ['Arkansas', 'Indiana', 'West_Virginia'] #'Arkansas', 'Indiana', 'West_Virginia'
years = ['1994','1996','1998','2000','2002','2004','2006','2008','2010','2012','2014','2016'] # '1994','1996','1998','2000','2002','2004','2006','2008','2010','2012','2014','2016'
for state in states:
    for year in years:
        # print ("Election data of " + state + " for the " + year + " election.")
        election = e.Election("United States House of Representatives Elections", year)
        election.districts = get_election_data(state, year)
        elections.append(election)

for election in elections:
    print (election.to_string())