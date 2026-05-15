import openreview
import config_ivo as c
import pandas as pd
import os
import time
import pprint

# DEFINITIONS
BASE_URL = 'https://api2.openreview.net'
YEAR='2026'
venue = f'IWAI{YEAR}'
venue_id    = f'IWAI/{YEAR}/Workshop'
SUBMISSION_INVITATION = f'{venue_id}/-/Submission'
ASSIGNMENT_INVITATION = f'{venue_id}/Reviewers/-/Assignment'
MSG_INVITATION=f'{venue_id}/-/Edit'
REVIEWER_GROUP = f'{venue_id}/Reviewers'
AUTHORS_GROUP = f'{venue_id}/Authors'

# CLIENT
client=openreview.api.OpenReviewClient(baseurl=BASE_URL,username=c.usr,password=c.pas)
venue_group = client.get_group(venue_id)
submission_str   = venue_group.content['submission_name']['value'] # this query results in text "Submission"
streams = ['1-comp','2-cogn','3-appl']
types=['1-paper','2-abstr']
submissions = client.get_all_notes(invitation=SUBMISSION_INVITATION, sort='number:asc', details='replies')

def list_of_all_authors():
    author_ids = set()
    for paper in submissions:
        ids = paper.content.get('authorids', [])["value"]
        for a_id in ids:
            if a_id and a_id != 'None':
                author_ids.add(a_id)
    print(f"Found {len(author_ids)} unique author IDs.")
    pprint.pprint(author_ids)
    print(f"Found {len(author_ids)} unique author IDs.")

def monitor():
    authP,authA = {},{}; i_p,i_a = 0,0
    for i,s in enumerate(submissions):
        subm_id = s.number
        aid = s.content['authorids']['value']    # List of all authors id's
        Typ=s.content.get("type")
        Strm=s.content.get("stream")
        typ = int(Typ["value"][0]) if not Typ==None else 1 # Fallback for previous IWAI editions without Type.
        typs = types[typ-1]
        tit = s.content['title']['value']
        kws = s.content['keywords']['value']
        # auth_prof = openreview.tools.get_profiles(client,aid)
        # auth[s.number]=ais
        if typ==1:
            i_p+=1;   authP[s.number]=[i_p,f"#{subm_id}",Strm, tit, aid, kws]
        else:
            i_a+=1;   authA[s.number]=[i_a,f"#{subm_id}",Strm, tit, aid, kws]
        pass
    print(f" ------------- {i_p} FULL PAPERS -------- ")
    pprint.pprint(dict(sorted(authP.items())))
    print(f" ------------- {i_a} EXT ABSTRACTS -------- ")
    pprint.pprint(dict(sorted(authA.items())))
    print(f" ----- TOTAL {i_p+i_a}:  {i_p} full papes and {i_a} ext abstracts -----")


if __name__ == '__main__':
    # list_of_all_authors()
    monitor()
