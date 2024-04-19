import requests
import json, csv
from datetime import datetime
import dateutil.parser
import exportghfunctions as egf
import credentials as cr

#which repo's issues will be listed

#which listed page from github will be exported (100 issues per page)
page = 3 
# accesstoken from GitHub, better use Fine grained

# repos api url
repos_url = str(cr.githubdomain)+""+str(cr.repo)+'/issues?status=open&per_page=100&page='+str(page) 
 #default header guided by GitHub
headers = {"Accept: application/vnd.github+json"}

'''
Create session with authentication
'''
# create a re-usable session object with the user creds in-built
try:
    gh_session = requests.Session()
    gh_session.headers = headers
    gh_session.auth = (cr.gitusername, cr.gittoken)
    print("Github session ok")
except:
    print("Can't create Github session")

try:

    # get the list of issues
    issues = json.loads(gh_session.get(repos_url).text)
    print("Issues fetched")
except: 
    print("Can't get issues")

'''
for loop to parse JSON response and insert issue with JIRA API into JIRA project
'''
try:

    for issue in issues:
        # Just for user eyes to see what kind of data has been fetched from GitHub
        print(str(issue["id"])+" "+str(issue["created_at"])+" "+str(egf.jiradate(issue["created_at"]))+" "+str(issue["state"])+"  [labels: "+str(egf.parselabels(issue["labels"]))+" ]"+str(issue["title"]))
        
        issuebody = egf.sanitizingissuebody(issue["body"], issue["html_url"])
        
        try:
            jiraissueid = egf.jiraissue(cr.projectid,issue["title"],issuebody, egf.parselabels(issue["labels"]), cr.assigneeid(issue["assignees"]))
            
            #TODO: comments. 

        except Exception as error:
            print("JIRA ISSUE CREATION FAILED", error)
except Exception as error:
    print("Can't loop issue data", error)
    