import json
import os
from urlmgr import UrlMgr
from typing import List
from lxml.html import fromstring, tostring


INPUT_FILE_PATH = os.getenv("INPUT_PATH")
OUTPUT_PATH = os.getenv("LOG_PATH")
ORIGIN_URL = "https://github.com/"


def url_maker(keywords: List, search_type: str = "repositories", page_num: int = 1) -> str:
    keys = "+".join(keywords)
    result = ORIGIN_URL + F"search?p={page_num}&q={keys}&type={search_type}"
    return result


def extract_repos_url(html_str: str, job_type: str) -> List:
    root = fromstring(html_str)
    repositories = []
    if job_type.upper() == "REPOSITORIES":
        for item in [div for div in root.xpath("//ul[@class=\"repo-list\"]/li/div[position()=2]/div/div/a")]:
            repositories.append(ORIGIN_URL + item.attrib['href'])
    elif job_type.upper() == "WIKIS":
        for item in [div for div in root.xpath("//div[@id=\"wiki_search_results\"]/div/div/div/a")]:
            repositories.append(ORIGIN_URL + item.attrib['href'])
    else:
        for item in [div for div in root.xpath("//div[@id=\"issue_search_results\"]/div/div/div/div[position()=2]/a")]:
            repositories.append(ORIGIN_URL + item.attrib['href'])
    return repositories


def get_repositories_from_job(keywords: List, job_type: str, page_num: int) -> List:
    url_str = url_maker(keywords, job_type, page_num)
    response = url_mgr.url_request(url_str)
    reposits = extract_repos_url(response, job_type)
    return reposits


def get_extra_info(url: str) -> str:
    resp = url_mgr.url_request(url)
    root = fromstring(resp)
    extras = {}
    key = None
    value = None
    idx = 0
    for item in [div for div in root.xpath("//div[@class=\"BorderGrid-cell\"]//li["
                                                     "@class=\"d-inline\"]//span")]:
        idx += 1
        if idx % 2:
            key = item.text
        else:
            value = item.text
        extras[key] = value
    return extras


def get_owner_from_repo_url(url: str) -> str:
    return url.split("/")[3]


def run_job(keywords: List, job_type: str):
    result = []
    page_num = 1
    repos = get_repositories_from_job(keywords, job_type, page_num)
    for repo_url in repos:
        repo_info = {"url": str(repo_url)}
        if job_type.upper() == "REPOSITORIES":
            extra_info = get_extra_info(str(repo_url))
            repo_info["extra"] = {"owner": get_owner_from_repo_url(repo_url), "language_stats": extra_info}
        result.append(repo_info)
    return result


if __name__ == '__main__':
    # Opening JSON file and Loading job file
    with open(INPUT_FILE_PATH) as json_file:
        data = json.load(json_file)
        url_mgr = UrlMgr(data['proxies'])

    print("start scrapping... ")
    try:
        results = run_job(data["keywords"], data["type"])
        with open(OUTPUT_PATH + 'output.json', 'w') as outfile:
            # json_string = json.dumps(results)
            json.dump(results, outfile, indent=4, sort_keys=True)
        print("successfully finished")
    except Exception as err:
        print(err)
