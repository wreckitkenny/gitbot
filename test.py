import gitlab
from gitlab.v4.objects import branches
from gitlab.v4.objects.projects import Project
import time, re

t0 = time.time()
gl = gitlab.Gitlab('http://10.10.175.153', private_token='xXskSy6W438sVeVmHr99')

cdProject = gl.projects.get(11)

# branch_list = [branch.name for branch in cdProject.branches.list()]
# filePath = [file['path'] for file in cdProject.repository_tree(recursive=True, all=True) if file['name'] == 'OWNERS'][0]

files = cdProject.repository_tree(recursive=True, all=True)
for file in files:
    if file['type'] == 'blob': 
        file_content = cdProject.files.raw(file_path=file['path'], ref='master')
        if "hub.vnpaytest.vn/library/web-frontend" in str(file_content):
            for i in file_content.decode().split('\n'):
                if 'tag' in i: 
                    i = re.sub(r'[\n\t ]', '', i)
                    i = re.search('(?<=:)(v)?(((\d(\.\d)+)-)?([a-z0-9]+)|[a-z]-)?([a-z0-9]+)',re.sub(r'[\n\t ]', '', i))
                    print(i.group(0))


# t1 = time.time()
# print(t1-t0)