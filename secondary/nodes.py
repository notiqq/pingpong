SEC_NODES = [{'name': 'secondary 1', 'url': 'http://localhost:5001'},
             {'name': 'secondary 2', 'url': 'http://localhost:5002'}]
urls = [node['url'] for node in SEC_NODES ]
print(urls)