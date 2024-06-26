import requests
import json, csv
from datetime import datetime
import dateutil.parser
from requests.auth import HTTPBasicAuth
import credentials as cr

'''
Functions for github
'''        

# same with labels
def parselabels(array):
    labels = []
    labels.append("Github")
    labels.append(str(cr.repo))

    for label in array:
        labels.append(label["name"])
    return labels

def jiradate(issuedate):
    #dd/MMM/yy h:mm a
    #newdate = date
    #newdate = datetime.strptime(issuedate, '%m/%d/%y')
    try:
        newdate = dateutil.parser.parse(issuedate).strftime('%d/%b/%y %-I:%M %p')
        #newdate = datetime.strptime(, '%m/%d/%y')
    except Exception as error:
        print("failure", error)

    return newdate

def parsecomments(comments):
    if not comments:
        return "No comments"
    else:
        commentstring = ""
        for comment in comments:
            #print(comment["created_at"])
            commentstring += comment["created_at"]
            commentstring += "\n"
            #print(comment["body"])
            commentstring += comment["body"]
            commentstring += "\n \n"
        return commentstring

    
def sanitizingissuebody(bodymessage,url):
    if bodymessage == None:
        return None
    else:
        try:
            cleanmessage = bodymessage.replace('"',"")
        except Exception as error: 
            print("cleaning message failed", error)

        try:    
            sealedmessage = ''+str(cleanmessage)+' \n \n'+str(url)
        except:
            print("Sealing message failed")

        return sealedmessage
    
def sanitizingcommentbody(bodymessage):
    if bodymessage == None:
        return None
    else:
        try:
            cleanmessage = str(bodymessage.replace('"',""))
        except Exception as error: 
            print("cleaning message failed", error)

        return cleanmessage

def jiraissue(projectid,issuetitle, issuedescription, labels,assigneeid):

    issuetype = "10015" #task
    #assigneeid = ""
    #issuedescription = ""
    #labels = ""
    if not assigneeid:
        assigneeid = None
    elif assigneeid == None:
        assigneeid = None
    else:    
        pass

    if not issuedescription:
        issuedescription = "No content"
    else:
        pass

    url = "https://"+cr.jiradomain+".atlassian.net/rest/api/3/issue"

    auth = HTTPBasicAuth(cr.jirausername, cr.jiraapitoken)

    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
    }

    payload = json.dumps( {
    "fields": {
        "assignee": {
            
            "id": assigneeid
        },

        "description": {
        "content": [
            {
            "content": [
                {
                "text": issuedescription,
                "type": "text",
                }
            ],
            "type": "paragraph"
            }
        ],
        "type": "doc",
        "version": 1
        },
        "issuetype": {
        "id": issuetype 
        },
        "labels": labels,
        "project": {

        "id": projectid
        },
        "summary": issuetitle,

    },
    "update": {}
    } )
    

    response = requests.request(
    "POST",
    url,
    data=payload,
    headers=headers,
    auth=auth
    )

    returnmessage = json.loads(response.text)
    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    return returnmessage["key"] 

def addcomments(jiraissueid,jiracomment):

    url = "https://"+str(cr.jiradomain)+".atlassian.net/rest/api/3/issue/"+str(jiraissueid)+"/comment"

    auth = HTTPBasicAuth(cr.jirausername, cr.jiraapitoken)

    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
    }

    payload = json.dumps( {
    "body": {
        "content": [
        {
            "content": [
            {
                "text": jiracomment,
                "type": "text"
            }
            ],
            "type": "paragraph"
        }
        ],
        "type": "doc",
        "version": 1
    }
    } )

    response = requests.request(
    "POST",
    url,
    data=payload,
    headers=headers,
    auth=auth
    )

    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

