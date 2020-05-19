# import NoFluffJobs
# import json
# import time

# configure link
tech = 'c++'  # 'java%20python%20...
city = 'warszawa'
page = 1
endPage = 1

#initialize
# start_time = time.perf_counter()

jobList = NoFluffJobs.Scrape(tech, city, 1, 1)

#write to file
# with open('JobFile.txt', 'w') as outfile:
#     json.dump(jobList, outfile)
# print('Job Offers List written to file. (3/3)')
#
# exec_time = time.perf_counter() - start_time
# print("Program took",round(exec_time, 0), "seconds to execute")
