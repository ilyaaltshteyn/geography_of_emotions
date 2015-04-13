#This script scrapes the last words and offender information summaries of 
#people executed on death row between 1982 and present time from the texas 
#department of criminal justice website.

import urllib2, urlparse, re, BeautifulSoup
import pandas as pd

#Write function that pulls html and returns a beautifulsoup object:
def soup_maker(url):
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup.BeautifulSoup(html)
    return soup

url = "http://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html"
soup = soup_maker(url)

#Pull all links out of <a href> tags and add appropriate prefix to them:
a_tags = soup.findAll('a')
links = []
prefix = "http://www.tdcj.state.tx.us/death_row/"
for tag in a_tags:
    # print tag
    try:
        #Make sure that the link is one of the ones about death row inmates,
        #in which case it would include "dr_info" as part of its url, then save
        #it to a list.
        if 'dr_info' in tag['href']:
            full_url = prefix + tag['href']
            links.append(full_url)
        else:
            continue
    except:
        continue


#Write function that pulls last statements when given a url:
def last_statement(location):
    if '.jpg' not in location:
        soup = soup_maker(location)
        p_tags = soup.findAll('p')
        assert len(p_tags) > 0
        for index, tag in enumerate(p_tags):
            if 'Last Statement' in tag.contents[0]:
                last_statement = p_tags[index + 1].contents
                break
        return last_statement[0]
    else:
        return "pull_error"

#Write function that returns the second part of a tag if it's not another tag, and the third part of the tag if the second part IS a tag.
def tag_parser(tag):
    """Tages tag and returns tag.contents[2] if it's a string, or 
    tag.contents[3] if the first one is NOT a string"""
    try:
        if isinstance(tag.contents[2], str):
            return tag.contents[2]
        else:
            return tag.contents[3]
    except:
        return "pull_error"

def exist_checker():
    """Checks whether or not the variables occupation, record and summary
    exist. If they don't, then returns pull_error for the ones that don't
    exist"""
    global occupation, record, summary
    try: 
        occupation
    except:
        occupation = 'pull_error'
    try:
        record
    except:
        record = 'pull_error'
    try:
        summary
    except:
        summary = 'pull_error'
    return occupation, record, summary

#Write function that pulls summary of incident and prior prison record from the
#offender information pages:
def summary_of_incident(location):
    if '.jpg' not in location:
        soup = soup_maker(location)
        p_tags = soup.findAll('p')
        assert len(p_tags) > 0
        for index, tag in enumerate(p_tags):
            if 'Prior Occupation' in tag.contents[0]:
                occupation = tag_parser(tag)
            if 'Prior Prison Record' in tag.contents[0]:
                record = tag_parser(tag)
            if 'Summary of Incident' in tag.contents[0]:
                summary = tag_parser(tag)
        try:
            occupation
        except:
            occupation = 'pull_error'
        try:
            record
        except:
            record = 'pull_error'
        try:
            summary
        except:
            summary = 'pull_error'
        return occupation, record, summary
    else:
        return "jpg_pull_error", "jpg_pull_error", "jpg_pull_error"

#Write a function that figures out whether the url is a last statement url or
#an offender info url:
def page_type(url_string):
    """Returns 1 if the page is a last statement page, returns 2 if the page is
    not a last statement page (it must therefore be an offender info page)"""

    if 'last' in url_string:
        return 1
    else:
        return 2

last_statements = []
occupations = []
records = []
summaries = []

for link in links:
    print page_type(link)
    if page_type(link) == 1:
        last_statements.append(last_statement(link))
    if page_type(link) == 2:
        occu, recor, summar = summary_of_incident(link)
        occupations.append(occu)
        records.append(recor)
        summaries.append(summar)




