import math
import pandas as pd

import requests
from bs4 import BeautifulSoup

jobids=[]
d={}
df=[]

target_url='https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=data%2Banalyst&location=Australia&start={}'

i = 0
res = requests.get(target_url.format(i))
soup=BeautifulSoup(res.text,'html.parser')
page_jobs=soup.find_all("li")

while(len(page_jobs) > 24 and i < 8):

    for x in range(0,len(page_jobs)):
        jobid = page_jobs[x].find("div",{"class":"base-card"}).get('data-entity-urn').split(":")[3]
        jobids.append(jobid)

    i = i+1
    res = requests.get(target_url.format(i))
    soup=BeautifulSoup(res.text,'html.parser')
    page_jobs=soup.find_all("li")

target_url='https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'
for job in range(0,len(jobids)):
    print(job)
    resp = requests.get(target_url.format(jobids[job]))
    soup=BeautifulSoup(resp.text,'html.parser')

    try:
        d["company"]=soup.find("div",{"class":"top-card-layout__card"}).find("a").find("img").get('alt')
    except:
        d["company"]=None

    try:
        d["job-title"]=soup.find("div",{"class":"top-card-layout__entity-info"}).find("a").text.strip()
    except:
        d["job-title"]=None

    try:
        d["level"]=soup.find("ul",{"class":"description__job-criteria-list"}).find("li").text.replace("Seniority level","").strip()
    except:
        d["level"]=None

    skills = ["sql", "python", "excel", " r ", ", r," , "tableau", "power bi", " ml ", ", ml,", "machine learning", "remote"]
    try:
        text = (d["job-title"] + " " + soup.find("div",{"class":"show-more-less-html__markup"}).get_text()).lower()
        for skill in skills:
            if skill in text:
                d[skill] = 1
            else:
                d[skill] = 0
    except:
        for skill in skills:
                d[skill] = None

    df.append(d)
    d={}

pd_df = pd.DataFrame(df)
pd_df.to_csv('linkedin_aus_da.csv', index=False, encoding='utf-8')
# print(pd_df)
