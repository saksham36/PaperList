#!/usr/bin/env python3
'''
Written by: Saksham Consul 04/05/2023
Script to get all papers of selected authors from 2022 onwards
'''

import os
import json
import requests
import tqdm
from serpapi import GoogleSearch

from professors import profs
from utils.data_handling import read_config, load_pickle, save_pickle


def get_papers(api_key, prof):
    '''Returns a list of papers for a given professor'''
    params = {
        "hl": "en",
        # "engine": "google_scholar_profiles",
        "engine": "google_scholar",
        "q": "\"CD+Manning\"",
        # "mauthors": "CD+Manning",
        "api_key": api_key,
        # "as_sdt": "0,5",
        "scisbd": 1,
        "as_ylo": 2022
    }

    cumulative_results = []
    for prof in profs:
        query = "\"" + prof + "\""
        params["q"] = query
        print(params)
        search = GoogleSearch(params)
        results = search.get_dict()
        try:
            organic_results = results["organic_results"]
            cumulative_results.extend(organic_results)
        except:
            print("No papers")
    return cumulative_results


def download_pdf(url, file_name, headers):
    '''Downloads the PDF from the given URL'''

    # Send GET request
    response = requests.get(url, headers=headers)

    # Save the PDF
    if response.status_code == 200:
        with open(file_name, "wb") as f:
            f.write(response.content)
    else:
        print("Could not download: ", url)
        # import pdb
        # pdb.set_trace()
        print(response.status_code)


def download_papers(papers):
    '''Downloads all the papers in the list'''
    # Define HTTP Headers
    headers = {
        "User-Agent": "Chrome/51.0.2704.103",
    }

    paper_list = tqdm.tqdm(papers)
    for paper in paper_list:
        link = paper['link']
        if os.path.exists('papers/'+paper['title']+'.pdf'):
            continue
        if 'Proceedings' in paper['title']:
            continue
        link_parts = link.split('/')
        # print(link_parts)
        if link_parts[2] == 'arxiv.org':
            paper['link'] = link.replace('abs', 'pdf') + '.pdf'

        elif link_parts[2] == 'www.biorxiv.org':
            paper['link'] = link.replace('abstract', 'full') + '.pdf'

        elif link_parts[2] == 'ieeexplore.ieee.org':
            paper['link'] = 'http://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&isnumber=&arnumber={}'.format(
                link_parts[5])

        elif link_parts[2] == 'dl.acm.org':
            paper['link'] = link.replace('abs', 'pdf')

        elif link_parts[2] == 'proceedings.neurips.cc':
            link1 = link.replace('hash', 'file')
            paper['link'] = link1.replace(
                'Abstract-Conference.html', 'Paper-Conference.pdf')

        elif link_parts[2] == 'ui.adsabs.harvard.edu':
            if 'arXiv' in link_parts[4]:
                sub_link_parts = link_parts[4].split('arXiv')
                paper['link'] = 'https://arxiv.org/pdf/' + \
                    sub_link_parts[1][:4]+'.'+sub_link_parts[1][4:-1] + '.pdf'

        elif link_parts[2] == 'aclanthology.org':
            paper['link'] = link[:-1] + '.pdf'

        elif link_parts[2] == 'proceedings.mlr.press':
            paper['link'] = link.replace(
                '.html', '/'+link_parts[-1].split('.')[0]+'.pdf')

        elif link_parts[2] == 'openreview.net':
            paper['link'] = link.replace('forum', 'pdf')

        elif link_parts[2] == 'navi.ion.org':
            paper['link'] = link.replace('abstract', 'full') + '.pdf'

        elif link_parts[2] == 'pubsonline.informs.org':
            paper['link'] = link.replace('abs', 'epdf')

        # No need additional formatting
        elif link_parts[2] in ['realworldml.github.io', 'yuxuanliu.com', 'zelikman.me', 'journals.sagepub.com',
                               'pcs-sim.github.io', 'asmedigitalcollection.asme.org', 'ai.stanford.edu', 'carloshinojosa.me',
                               'edarxiv.org', 'knowledge-nlp.github.io', 'msl-dev.stanford.edu']:
            pass

        # Not downloading this paper
        # TODO: Add Springer API
        elif link_parts[2] in ['digitalcommons.uncfsu.edu', 'history.siggraph.org',
                               'www.ahajournals.org', 'research.google', 'link.springer.com', 'direct.mit.edu',
                               'www.emerald.com', 'molecular-cancer.biomedcentral.com', 'jov.arvojournals.org',
                               'www.medrxiv.org', 'europepmc.org', 'www.worldscientific.com', 'www.jmir.org',
                               'www.annualreviews.org', 'papers.ssrn.com', 'www.sciencedirect.com',
                               'journals.plos.org', 'www.cell.com', 'onlinelibrary.wiley.com', 'www.academia.edu',
                               'bmcmusculoskeletdisord.biomedcentral.com', 'www.spiedigitallibrary.org', 'www.mdpi.com',
                               'www.nature.com', 'pdfslide.us', 'www.ion.org']:
            continue

        # File format not recognized
        else:
            print(f"Link format not recognized. Skipping {link}")
        download_pdf(paper['link'], 'papers/'+paper['title']+'.pdf', headers)


def main():
    '''Fetch all papers from list of professors from 2022 onwards'''
    try:
        cumulative_results = load_pickle('papers.pkl')
    except Exception as e:
        print(e, "Papers list pickle not found. Generating papers list")
        api_key = read_config()["api_key"]
        cumulative_results = get_papers(api_key, profs)
        save_pickle(cumulative_results, 'papers.pkl')

    # Download PDFs
    download_papers(cumulative_results)
    try:
        os.mkdir('papers')
    except:
        pass


if __name__ == "__main__":
    main()
