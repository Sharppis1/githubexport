# githubexport

# export-github.py
- Tämä ajetaan python3 export-github.py
- Tarkista ensiksi
    - repo -muuttuja ja aseta se vastaamaan omaa repoa 
    - projectid -muuttuja pitää vastata sitä jiraprojectia johon issuet luodaan
    - page -muuttuja riippuu githubin issueiden määrästä jos issueita on 300 joutuu skriptin ajamaan kolme kertaa, ekalla page = 1, tokalla page = 2 jne. github rajoittaa issuelistauksen 100 issueeseen per haku.



Oletuksena kaikki menee issuetype task (10015), jos haluaa muuttaa niin jiraissue() funkkariin pitää muuttaa oikea issuetypeid

# credentials.py
tämän joudut luomaan itsellesi, seuraavilla muuttujilla

- gitusername
- gittoken
- jirausername
- jiraapitoken
- githubdomain
- jiradomain
- projectid
- repo

lisää myös credentials.py:hyn myös seuraava funktio, johon listaat mäppäystarkistuksen jira(assigneeid) vs github(displayedname)

def assigneeid(array):
    match assignee["login"]:
        case "githubusername":
            return "assigeeid"
        case _:
            None

assigneeid tarkistetaan vielä toistamiseen ja varmistetaan että jos assigneeidtä ei löydy niin issue luodaan, mutta unassignedina. 

Githubin labelit eivät saa sisältää välejä, jira mököttää niistää

assigneeid löytyy user managementista henkilön profiili URL:sta

projectid löytyy projektien selaamisnäkymästä taas projektin urlista