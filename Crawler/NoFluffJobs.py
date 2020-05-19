from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.error import URLError
import requests
from lxml import html

# collection of all classes in job offers
noFluffJobsClasses = [
    'posting-list-item posting-list-item--bigData',
    'posting-list-item posting-list-item--security',
    'posting-list-item posting-list-item--other',
    'posting-list-item posting-list-item--frontend',
    'posting-list-item posting-list-item--businessAnalyst',
    'posting-list-item posting-list-item--agile',
    'posting-list-item posting-list-item--productManagement',
    'posting-list-item posting-list-item--backend',
    'posting-list-item posting-list-item--mobile',
    'posting-list-item posting-list-item--fullstack',
    'posting-list-item posting-list-item--gaming',
    'posting-list-item posting-list-item--itAdministrator',
    'posting-list-item posting-list-item--businessIntelligence',
    'posting-list-item posting-list-item--devops',
    'posting-list-item posting-list-item--testing',
    'posting-list-item posting-list-item--support',
    'posting-list-item posting-list-item--embedded',
    'posting-list-item posting-list-item--artificialIntelligence',
    'posting - list - item posting - list - item - -ux',
    'posting-list-item posting-list-item--ux',
    'posting-list-item posting-list-item--projectManager'
]

# Gets list of links to jobs
def getLinks(bs):
    myList = []
    linkList = bs.find('div', {'container mb-5'}).findAll('a', class_=noFluffJobsClasses, href=True)

    for link in linkList:
        myList.append('https://nofluffjobs.com'+str(link.attrs['href']))
    return myList

#get seniority level (subpage)
def getSeniority(linkList):
    myList = []
    for link in linkList:
        html = urlopen(link)
        bs = BeautifulSoup(html.read(), 'html.parser')
        
        seniority = bs.find('div', {'col star-section text-center active'}).findNext('p')
        myList.append(seniority.get_text())
    return myList

#get description (subpage)
def getDescription(linkList):
    myList = []
    for link in linkList:
        content = html.fromstring(requests.get(link).content)
        desc = content.xpath('/html/body/nfj-root/nfj-layout/nfj-main-content/div/div/div[1]/nfj-posting-details/nfj-main-loader/section/div[2]/div[1]/div[1]/nfj-posting-description/div/p/text()')
        myList.append(desc)
    return myList

# returns years of experience required in job description (if available)
def getExperience(descList):
    myList = []
    str_want = '1,2,3,4,5,6,7,8,9,0,-'
    for desc in descList:
        mDesc = str(desc)

        yearWordPos = mDesc.find('year')
        if yearWordPos < 0:
            yearWordPos = mDesc.find('lat')
            if yearWordPos < 0:
                yearWordPos = mDesc.find('let')

        if yearWordPos < 0:
            myList.append('-')
        else:
            exp_part = mDesc[yearWordPos - 4:yearWordPos]
            exp = [s for s in exp_part if s in str_want]
            exp = ''.join(exp)
            try:
                if int(exp) > 20: exp = '-'
            except:
                pass

            myList.append(exp)

    return myList

# count job offers on site
def countOffers(bs):
    offersList = bs.findAll('h4', {'posting-title__position'})
    offersList = len(offersList)
    return offersList

# Get list of job titles
def getTitle(bs):
    myList = []
    jobTitleList = bs.findAll('h4', {'posting-title__position'})
    for title in jobTitleList:
        myList.append(title.get_text().replace(' NOWA',''))
    return myList

# Get list of salaries - different method used as the salary might be missing
def getSalary(bs):
    myList = []
    offersList = bs.find('div', {'container mb-5'}).findAll('a', class_=noFluffJobsClasses)
    for i in range(0,len(offersList)):
        if offersList[i].find('span','text-truncate badgy salary btn btn-outline-secondary btn-sm'):
            myList.append(offersList[i].find('span','text-truncate badgy salary btn btn-outline-secondary btn-sm').get_text())
        else:
            myList.append('N/A')

    return myList

# Get list Employer names
def getEmployer(bs):
    myList = []
    employerList = bs.findAll('span', {'posting-title__company d-none d-lg-inline'})
    for name in employerList:
        myList.append(name.get_text().replace('w ','',1))
    return myList

# open&connect to URL -> also serves as run method generating the final output
def Scrape(tech, city, starting_page: int, ending_page: int):
    generalList = []
    generalList.append('Job Title;;;Employer Name;;;Salary;;;Link;;;Seniority;;;describtion;;;experience')

    for i in range(starting_page, ending_page+1):
        print("Trying crawling on page "+ str(i) + "/" + str(ending_page))
        if tech:
            url = 'https://nofluffjobs.com/pl/jobs/' + city + '/' + tech + '?criteria=city%3D' + \
                city + '%20' + tech + '&page=' + str(i)
        else:
            url = 'https://nofluffjobs.com/pl/jobs/' + city + '?criteria=city%3D' + \
                  city + '&page=' + str(i)

        try:
            html = urlopen(url)
            print("HTML found (1/3)")
        except HTTPError as e:
            print('HTML does not exist')
            break
        except URLError as e:
            print("Server not found")
            break
        else:
            print("Successfully connected to the server! (2/3)")

        bs = BeautifulSoup(html.read(), 'html.parser')

        title = getTitle(bs)
        employer = getEmployer(bs)
        salary = getSalary(bs)
        link = getLinks(bs)
        seniority = getSeniority(link)
        desc = getDescription(link)
        experience = getExperience(desc)
        for i in range(countOffers(bs)):
            jobOffer = "%s;;;%s;;;%s;;;%s;;;%s;;;%s;;;%s" % (title[i], employer[i], salary[i],
                                                 link[i], seniority[i], desc[i], experience[i])
            generalList.append(jobOffer)

    return generalList

