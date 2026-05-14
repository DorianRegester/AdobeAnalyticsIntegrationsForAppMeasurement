import os
import requests
import datetime

# Environment Variables
PAT = os.getenv('PAT_TOKEN')
RSID = os.getenv('ADOBE_RSID')
TRACKING_SERVER = os.getenv('ADOBE_TRACKING_SERVER')

def send_to_adobe(repo_name, views, clones, stars, forks, file_path=None):
    # XML Payload for Data Insertion API
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S-00:00")
    
    # Constructing the events string
    events = f"event1={views},event2={clones},event3={stars},event4={forks}"
    
    xml_payload = f"""<?xml version="1.0" encoding="UTF-8"?>
    <request>
        <sc_xml_ver>1.0</sc_xml_ver>
        <reportSuiteID>{RSID}</reportSuiteID>
        <visitorID>github_worker_001</visitorID>
        <timestamp>{timestamp}</timestamp>
        <pageName>github:repo:view</pageName>
        <eVar1>{repo_name}</eVar1>
        {f'<eVar2>{file_path}</eVar2>' if file_path else ''}
        <events>{events}</events>
    </request>"""

    url = f"https://{TRACKING_SERVER}/b/ss/{RSID}/6" # '6' specifies XML format
    headers = {'Content-Type': 'application/xml'}
    
    response = requests.post(url, data=xml_payload, headers=headers)
    return response.status_code

def sync_portfolio():
    headers = {"Authorization": f"token {PAT}"}
    # Fetch up to 100 repos
    repos = requests.get("[https://api.github.com/user/repos?per_page=100&type=owner](https://api.github.com/user/repos?per_page=100&type=owner)", headers=headers).json()

    for repo in repos:
        name = repo['full_name']
        print(f"Processing Adobe Sync: {name}")

        # Fetch Traffic Metrics
        v_data = requests.get(f"[https://api.github.com/repos/](https://api.github.com/repos/){name}/traffic/views", headers=headers).json()
        daily_v = v_data.get('views', [])[-1].get('count', 0) if v_data.get('views') else 0

        c_data = requests.get(f"[https://api.github.com/repos/](https://api.github.com/repos/){name}/traffic/clones", headers=headers).json()
        daily_c = c_data.get('clones', [])[-1].get('count', 0) if c_data.get('clones') else 0

        # Send Aggregate Repo Hit
        send_to_adobe(name, daily_v, daily_c, repo['stargazers_count'], repo['forks_count'])

        # Fetch and Send Path Specific Data (Top 3 paths)
        paths = requests.get(f"[https://api.github.com/repos/](https://api.github.com/repos/){name}/traffic/popular/paths", headers=headers).json()
        for p in paths[:3]:
            send_to_adobe(name, p['count'], 0, 0, 0, file_path=p['path'])

if __name__ == "__main__":
    sync_portfolio()
