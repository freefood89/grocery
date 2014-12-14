import requests
import htmlParser as html
import re
import json

def get_times_flyers(url = 'http://www.timessupermarkets.com/2013/01/01/our-locations-on-oahu-maui-kauai/'):
	r = requests.get(url)
	print('Getting Times Stores:', r.status_code)
	contents = html.get_elements(r.text, 'article', {'id':'the-content'})
	print(len(contents))

	stores = []

	for span in html.get_elements(contents[0], 'span'):
		store = {}
		for storeName in html.get_elements(span,'strong'):
			store['name'] = re.sub(r'<strong>|</strong>|&nbsp|<.*?</.*?>', '', storeName)
		for anchor in html.get_elements(span,'a',contains='Weekly Ads'):
			store['ad home'] = html.get_link(anchor)	

		if 'ad home' in store and 'name' in store:	
			r = requests.get(store['ad home'])
			print(store['name']+': ',end='')
			div = html.get_elements(r.text,'div',{'class':'pagination'})
			if div:
				store['pages'] = [html.get_link(anchor) for anchor in html.get_elements(div[0],'a')]
				print('found',len(store['pages']),'pages')
			else:
				print('no flyers found')
			if 'pages' in store:
				stores.append(store)

	json.dump(stores,open('timesAds.json','w'))
	return stores

if __name__ == '__main__':
	print('Service Started')

	stores = json.load(open('timesAds.json'))
	new_stores = []
	for store in stores:
		store['flyer images'] = []
		for link, pageIndex in zip(store['pages'] , range(len(store['pages']))):
			r = requests.get(link)
			images = html.get_elements(r.text,'img',{'id':'PageImage'})
			if images:
				r = requests.get(html.get_link(images[0]))
				filename = 'times_flyers/{}_{}.jpg'.format(store['name'],pageIndex)
				store['flyer images'].append(filename)
				with open(filename,'wb') as outfile:
					outfile.write(r.content)
		new_stores.append(store)

	json.dump(new_stores,open('timesAds.json','w'))

	# get_times_flyers()
	# for store in json.load(open('timesAds.json')):
	# 	r = requests.get(store['ad home'])
	# 	print(store['name'])
	# 	for div in html.get_elements(r.text,'div',{'class':'pagination'}):
	# 		for anchor in html.get_elements(div,'a'):
	# 			print(html.get_link(anchor))



