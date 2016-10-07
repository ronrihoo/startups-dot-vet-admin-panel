# Brief: scrapes https://www.vip.vetbiz.gov/Public/Search/Default.aspx
#
# Written for startups.vet
#
# 2016 Oct 01   -   Ronald Rihoo
#

import time

import requests

from admin_panel.scanners import pathmaker


def modify_url(index=0):
    url = 'https://www.vip.vetbiz.gov/Public/Search/ExportSearchResults.aspx?SCID=3369234&PageIndex=' \
          + str(index) + '&PageSize=100'
    return url


def get_urls(iterations):
    urls = []
    for iteration in range(iterations):
        urls.append(modify_url(iteration))
    return urls


def generate_filenames(quantity):
    filenames = []
    for number in range(quantity):
        filenames.append('vip.vetbiz.gov.set' + str(number + 1) + '.xls')
    return filenames


# TODO: make this an asynchronous task or at least create an output console to show user what's happening.
#
# Note: as a result of the courtesy mechanism, this process currently takes 2-3 minutes, which is a long time
#       to sit around waiting for the webpage to reload.
#
def download_files(links, filenames):
    for index, link in enumerate(links):
        print("Downloading " + filenames[index] + " from " + link)
        req = requests.get(link, verify=False)
        with open(filenames[index], "wb") as newfile:
            newfile.write(req.content)
        time.sleep(2)  # courteous conduct
        # *for Python 3
        # try:
        #     urllib2.urlopen(link, filenames[index])
        # except:
        #     print("Download failed...")
        # time.sleep(2)   # courteous conduct


def run():
    pathmaker.make_path('admin_panel/scanners/vetbiz/excel_files')
    links = get_urls(91)
    filenames = generate_filenames(len(links))
    download_files(links, filenames)
    print("All downloads completed.")
