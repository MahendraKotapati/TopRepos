from django.shortcuts import render
from django.contrib import messages
from datetime import datetime
import requests

# Create your views here.
token =  'ba5fe324148059036bf42be4d4bce87f5e7e6c22'   # your token no
#https://api.github.com/orgs/microsoft/repos?&sort=full_name&order=desc&page=30

def get_top_n_repos(request,organization_name,n):

    now_start = datetime.now()
    headers = {'Authorization': f'token {token}'}
    url = 'https://api.github.com/search/repositories?q=org:'+organization_name+'&sort=forks&order=desc&per_page=100&page=1'
    res = requests.get(url,headers = headers)
    repos = []

    if('items' not in res.json().keys()):    # requests.get return dict is no organization is found
        messages.error(request,'Organization : "'+ organization_name + '" is not present')
        return None
    

    for repo in res.json()['items']:
        repos.append(repo) 

    while 'next' in res.links.keys():   # this to deal with pagination ,for every page we make request and check next page is there or not
        res = requests.get(res.links['next']['url'],headers = headers)
        for repo in res.json()['items']:
            repos.append(repo)

        if(len(repos)>n):
            break

    if(len(repos)>n):
        repos = repos[:n]

    data = []
    for repo in repos:
            data.append([repo['forks_count'],repo['contributors_url'],repo['html_url']])  # taking only required fields 
    return data


def get_top_m_contributors_of_a_repo(request,repo,m):

    page_size = 100
    headers = {'Authorization': f'token {token}'}
    url = repo[1]+'?q=contributions&order=desc&per_page='+str(page_size)
    res = requests.get(url,headers = headers) 
    contributors_list = res.json()

    while 'next' in res.links.keys():   # this to deal with pagination , if result cannot fit it in one page 
        if(len(contributors_list)>=m):
            break
        res = requests.get(res.links['next']['url'],headers = headers)
        contributors_list.extend(res.json())


    if(len(contributors_list)>m):
        contributors_list = contributors_list[:m]

    curr_repo = {}  # dictionary to store current repostiory contributors and their commit count , key is contrinutor name 
    for contributor in contributors_list:
        curr_repo[contributor['login']] = [contributor['contributions'],contributor['html_url']]
    
    return curr_repo


def index(request):

    if(request.POST):
        organization_name = request.POST['organization']
        n = int(request.POST['n'])
        m = int(request.POST['m'])

        if(n<=0):
            messages.error(request,'repositories must >0')
            return render(request,'input.html')

        if(m<=0):
            messages.error(request,'committees must >0')
            return render(request,'input.html')

        now_start = datetime.now()
        data = get_top_n_repos(request,organization_name,n)   # get_repos top n repos for an organization
        if(data is None):
            return render(request,'input.html')

        print('response time  for fetching repos: ',datetime.now()-now_start)
        
        top_repos = {}  # dictionary  to store top repos

        if(len(data)<n):  # if an organization has less than n repositories
            n = len(data)
            messages.error(request,'we only have '+str(n)+' repos for '+organization_name)

        for repo in data:  # data[:n] top n repositories
            curr_repo = get_top_m_contributors_of_a_repo(request,repo,m)
            top_repos[repo[2]] = curr_repo  # storing current repo by url as key in top_repos dictionary

        return render(request,'index.html',{'top_repos':top_repos,'m':m,'n':n,'organization_name':organization_name})
    else:
        return render(request,'input.html')

