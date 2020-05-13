import NoFluffJobs
import json

# configure link
tech = 'python'  # 'java%20python%20...
city = 'krakow'
page = 1
endPage = 1

#initialize
jobList = NoFluffJobs.Scrape(tech, city, page, endPage)

#write to file
with open('JobFile.txt', 'w') as outfile:
    json.dump(jobList, outfile)
print('Job Offers List written to file. (3/3)')


