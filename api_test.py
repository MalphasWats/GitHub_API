import requests
import json

from settings import token

SITE_BRANCH = 'master'
COMMITTER = {'name': 'MalphasWats', 'email': 'malphas@subdimension.co.uk'}

username = 'MalphasWats'
repo = 'GitHub_API'

"""filename = "README.md"

URL = 'https://api.github.com/repos/%s/%s/contents/%s' % (username, repo, filename)
		
header = {
	'Authorization': 'token %s' % token,
	'User-Agent': username
}

get_data = {
	'path': filename,
	'ref': SITE_BRANCH
}

response = requests.get(URL, headers=header, params=get_data)
response_json = response.json()

print response.status_code, response_json['sha']"""


#get the current commit object
print "Getting current Commit"
URL = 'https://api.github.com/repos/%s/%s/git/refs/heads/%s' % (username, repo, SITE_BRANCH)
header = {
	'Authorization': 'token %s' % token,
	'User-Agent': username
}

response = requests.get(URL, headers=header)
response_json = response.json()
print response.status_code
print response_json['object']['sha']
print 
current_commit_sha = response_json['object']['sha']


#retrieve the tree it points to
#/repos/:owner/:repo/git/trees/:sha
print "Getting commit tree"
URL = 'https://api.github.com/repos/%s/%s/git/trees/%s' % (username, repo, current_commit_sha)
header = {
	'Authorization': 'token %s' % token,
	'User-Agent': username
}

response = requests.get(URL, headers=header)
response_json = response.json()
print response.status_code
print response_json['sha']
print
current_tree_sha = response_json['sha']

#retrieve the content of the blob object that tree has for that particular file path
#change the content somehow and post a new blob object with that new content, getting a blob SHA back
# (or create a whole new blob for a new file?!?!)
print "Creating blobs"
file1 = {'name': 'file1.md',
		 'content': u"#File 1\n\n This is file 1. Modified\n"}
		 
file2 = {'name': 'file2.md',
		 'content': u"#File 2\n\n This is file 2. Modified\n"}
		 
URL = 'https://api.github.com/repos/%s/%s/git/blobs' % (username, repo)
header = {
	'Authorization': 'token %s' % token,
	'User-Agent': username
}

data = {
	'content': file1['content'],
	'encoding': 'utf-8'
}

response = requests.post(URL, headers=header, data=json.dumps(data))
response_json = response.json()
print response.status_code
print response_json['sha']
file1['sha'] = response_json['sha']
print

data = {
	'content': file2['content'],
	'encoding': 'utf-8'
}

response = requests.post(URL, headers=header, data=json.dumps(data))
response_json = response.json()
print response.status_code
print response_json['sha']
file2['sha'] = response_json['sha']
print


#post a new tree object with that file path pointer replaced with your new blob SHA getting a tree SHA back
print "Creating tree"
URL = 'https://api.github.com/repos/%s/%s/git/trees' % (username, repo)
header = {
	'Authorization': 'token %s' % token,
	'User-Agent': username
}

tree = [
		{'path': file1['name'],
		 'mode': "100644",
		 'type': "blob",
		 'sha': file1['sha']
		},
		{'path': file2['name'],
		 'mode': "100644",
		 'type': "blob",
		 'sha': file2['sha']
		}
	   ]

data = {
	'base_tree': current_tree_sha,
	'tree': tree
	}

response = requests.post(URL, headers=header, data=json.dumps(data))
response_json = response.json()
print response.status_code
print response_json['sha']
print
new_tree_sha = response_json['sha']
#create a new commit object with the current commit SHA as the parent and the new tree SHA, getting a commit SHA back
print "Commiting Tree"
URL = 'https://api.github.com/repos/%s/%s/git/commits' % (username, repo)
header = {
	'Authorization': 'token %s' % token,
	'User-Agent': username
}

data = {
	'message': "Test Commit 3",
	'tree': new_tree_sha,
	'parents': [current_commit_sha]
}

response = requests.post(URL, headers=header, data=json.dumps(data))
response_json = response.json()
print response.status_code
print response_json['sha']
print
new_commit_sha = response_json['sha']

#update the reference of your branch to point to the new commit SHA
print "Updating branch ref"
URL = 'https://api.github.com/repos/%s/%s/git/refs/heads/%s' % (username, repo, SITE_BRANCH)
header = {
	'Authorization': 'token %s' % token,
	'User-Agent': username
}

data = {
	'sha': new_commit_sha,
	'force': 'true'
}

response = requests.patch(URL, headers=header, data=json.dumps(data))
print response.status_code, response.content
print "done"