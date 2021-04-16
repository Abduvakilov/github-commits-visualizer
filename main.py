#!/usr/bin/env python3

import requests, datetime, argparse, sys, webbrowser, os

DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
DATE_OUTPUT_FORMAT = '%y-%m-%d'

DEFAULT_REPOSITORY = 'tiangolo/fastapi'
DEFAULT_DAYS = 30

HEADERS = {
	'Accept': 'application/vnd.github.v3+json'
}

def get_github_commit(link):
	r = requests.get(link, headers=HEADERS, params=params)
	commits = r.json()

	next_link = r.links.get('next', {}).get('url')
	commit_data = {}
	for commit in commits:
		author = (commit.get('commit') or {}).get('author') or {}
		date = datetime.datetime.strptime(author['date'], DATE_FORMAT)
		date_author_name = date.strftime(DATE_OUTPUT_FORMAT) + author['name']
		commit_data[date_author_name] = commit_data.get(date_author_name, 0) + 1
	return commit_data, next_link

def pretty_json(data):
	import json
	print(json.dumps(data, indent=4, sort_keys=True))

def add_dict_values(dict1, dict2):
	for key, value in dict2.items():
		dict1[key] = dict1.get(key, 0) + value
	return dict1

def js_var(author_list):
	res = 'var data = ['
	first = True
	for date_author_name, commit_count in author_list.items():
		date = date_author_name[0:len(DATE_OUTPUT_FORMAT)]
		author_name = date_author_name[len(DATE_OUTPUT_FORMAT):]
		if not first:
			res += ','
		else:
			first = False
		res += ('{"author_name":"' + author_name + '",'
				'"date":"' + date + '",'
				'"commit_count":' + str(commit_count) + '}')
	return res+']'

def write_to_file(output, template_filename, output_filename):
	lines = []
	line_number = 1
	with open(template_filename, "r") as f:
	    lines = f.readlines()
	with open(output_filename, "w") as f:
	    for line in lines:
	    	if line_number == 33:
	    		f.write(output + '\n')
	    	else:
	    		f.write(line)
	    	line_number += 1

if __name__ == '__main__':

	parser = argparse.ArgumentParser(prog=sys.argv[0], usage='%(prog)s [options]')
	parser.add_argument('-r', '--repository', default=DEFAULT_REPOSITORY, required=False)
	parser.add_argument('-d','--days', default=DEFAULT_DAYS, help='For how many days to look commits for', type=int, required=False)
	parser.add_argument('-o','--output', default='output.html', required=False)
	parser.add_argument('-t','--template', default='template.html', required=False)
	args = parser.parse_args()

	repository = args.repository
	days = args.days
	output_filename = args.output
	template_filename = args.template

	until = datetime.datetime.today()
	since = until - datetime.timedelta(days=days)

	params = {
		'since': since.strftime(DATE_FORMAT),
		'until': until.strftime(DATE_FORMAT),
		'per_page': 100
	}

	res_commit_data = {}
	next_link = f'https://api.github.com/repos/{repository}/commits'
	while True:
		print(next_link)
		commit_data, next_link = get_github_commit(next_link)
		res_commit_data = add_dict_values(res_commit_data, commit_data)
		if not next_link:
			break
	output = js_var(res_commit_data)
	write_to_file(output, template_filename, output_filename)
	print('Commits graph has been created and it will be opened in a browser')
	webbrowser.open('file://' + os.path.realpath(output_filename))
	print(output_filename)
