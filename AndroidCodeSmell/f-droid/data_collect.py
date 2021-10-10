# -*- coding: utf-8 -*-
""" 
@Author:MaoMorn
@Time: 2020/07/10
@Description: 
"""

import requests
import json
from bs4 import BeautifulSoup
import collections

base_url = "https://f-droid.org"
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
}


def parse_index():
    url = "https://f-droid.org/zh_Hans/packages/"
    data = requests.get(url, headers=header).content.decode('utf-8')
    print("请求  %s  成功" % url)
    soup = BeautifulSoup(data, 'html.parser')
    categories_div = list(soup.find("div", class_="post-content"))
    categories = collections.defaultdict(dict)
    for i in range(1, len(categories_div), 6):
        category = str(categories_div[i].text)
        category_url = base_url + categories_div[i + 4].find('a')['href']
        categories[category]['url'] = category_url
        categories[category]['apps'] = parse_category(category_url)
        print("  %s  分析完成" % category)
        save2json(categories)
    print("  %s  分析完成" % url)


def parse_category(url):
    packages = []
    data = requests.get(url, headers=header).content.decode('utf-8')
    print("请求  %s  成功" % url)
    soup = BeautifulSoup(data, 'html.parser')
    packages_div = list(soup.find("div", id="package-list"))
    for i in range(1, len(packages_div), 2):
        info_div = list(packages_div[i].find('div'))
        package = {
            "name": info_div[1].text.strip(),
            "desc": info_div[3].find('span').text,
            "url": base_url + packages_div[i]['href'],
        }
        # package['size'] = parse_package(package['url'])
        packages.append(package)
    print("  %s  分析完成" % url)
    return packages


def parse_package(package):
    url = package['url']
    data = requests.get(url, headers=header).content.decode('utf-8')
    print("请求  %s  成功" % url)
    soup = BeautifulSoup(data, 'html.parser')
    package_links = soup.find("ul", class_="package-links").findAll('a')
    repository = ""
    for link in package_links:
        if link.text == "源代码":
            repository = link["href"]
            break
    package_version = soup.find("li", class_="package-version")
    if repository == "":
        repository = package_version.find("p", class_="package-version-source").find("a")["href"]
    version_header = package_version.find("div", "package-version-header")
    ver_names = list(version_header.findAll("a"))
    version = "%s(%s)" % (ver_names[0]["name"], ver_names[1]["name"])
    size = list(package_version.find("p", "package-version-download"))[2].strip()
    package["repo_link"] = repository
    package["latest_ver"] = version
    package['size'] = size


def set_package_attrs():
    filename = "f-droid.json"
    file = open(filename, 'r', encoding='utf-8')
    data = json.load(file)
    file.close()
    for category in data:
        for package in data[category]["apps"]:
            if package.get("repo_link") is None or package["repo_link"] == "" or package["repo_link"].endswith(".yml"):
                try:
                    parse_package(package)
                except:
                    save2json(data)
    save2json(data)
    print("保存到文件  %s  成功" % filename)


def save2json(data):
    filename = "f-droid.json"
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)
        file.close()
    print("保存到文件  %s  成功" % filename)


def analysis_json():
    filename = "f-droid.json"
    file = open(filename, 'r', encoding='utf-8')
    data = json.load(file)
    keys = data.keys()
    count = 0
    big_count = 0
    for i in keys:
        count += len(data[i]['apps'])
        print("%-10s共有%-d项" % (i, len(data[i]['apps'])))
        for app in data[i]["apps"]:
            app_size = app["size"].split()
            if len(app_size) > 1 and app_size[1] == "MiB" and eval(app_size[0]) >= 10:
                big_count += 1
    file.close()
    print("共计%d" % count)
    print("大应用共计%d" % big_count)


if __name__ == "__main__":
    # set_package_attrs()
    # parse_index()
    analysis_json()
