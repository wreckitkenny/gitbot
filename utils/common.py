import os, logging, re, gitlab

def changeContent(file, old, new):
    with open(file, 'r') as f:
        content = f.read()
        content = content.replace(old, new)
    with open(file, 'w') as f:
        f.write(content)

def changeTag(gl, resource, cdProject, oldTag, newTag, binPath, location, branchName):
    # Check directory existing
    cdFolder = '/'.join(location[0].split('/')[:-1])
    if os.path.isdir(binPath+'/'+cdFolder) == False: os.makedirs(binPath+'/'+cdFolder)

    # Download raw file
    logging.info("Gitbot is downloading CD file containing tag [{}].".format(oldTag))
    with open(binPath+'/'+location[0], 'wb') as f:
        cdProject.files.raw(file_path=location[0].strip(), ref='master', streamed=True, action=f.write)

    # Change content
    logging.info("Gitbot is changing tag from old tag [{}] to new tag [{}].".format(oldTag, newTag))
    changeContent(binPath+'/'+location[0], oldTag, newTag)

    # Commit changes
    data = {
        'branch': branchName,
        'commit_message': 'Change tag',
        'actions': [
            {
                'action': 'update',
                'file_path': location[0].strip(),
                'content': open(binPath+'/'+location[0]).read(),
            }
        ]
    }
    logging.info('Gitbot is committing new change to branch [{}].'.format(branchName))
    cdProject.commits.create(data)

    # Create merge request
    if branchName == newTag:
        assignees = getApprovers(gl, cdProject, cdFolder)
        logging.info('Gitbot is creating a merge request for new branch [{}]'.format(branchName))
        mr = cdProject.mergerequests.create({'source_branch':branchName, 'target_branch':'master', 'title':'Vnpaybot has released {}'.format(resource), 'assignee_ids':assignees})
        mr.approval_rules.create({"name": "Production MR Policy", "approvals_required": 2, "rule_type": "regular","user_ids": assignees})

    # Complete
    logging.info('Gitbot has finished changing old tag [{}] to new tag [{}].'.format(oldTag, newTag))

def checkEnvironment(gl, parser, pushedTag):
    env = cdProject = ''
    id_dev = parser.get('WORKLOAD', 'DEV_DEPLOYMENT')
    id_staging = parser.get('WORKLOAD', 'STAGING_DEPLOYMENT')
    id_prod = parser.get('WORKLOAD', 'PROD_DEPLOYMENT')
    if pushedTag.split('-')[0] == 'd' and checkProjectID(gl, id_dev) == 1: 
        env = 'dev'
        cdProject = gl.projects.get(id_dev)
    # elif re.match('(v)?((\d\.){2}\d)', pushedTag.split('-')[0]) != None and checkProjectID(gl, id_staging) == 1:
    if pushedTag.split('-')[0] == 't' and checkProjectID(gl, id_staging) == 1:
        env = 'test'
        cdProject = gl.projects.get(id_staging)
    if pushedTag.split('-')[0] == 'm' and checkProjectID(gl, id_prod) == 1:
        env = 'prod'
        cdProject = gl.projects.get(id_prod)
    return(env,cdProject)

def checkProjectID(gl, id):
    try:
        gl.projects.get(id)
    except gitlab.exceptions.GitlabGetError:
        logging.error("ProjectID {} is not existing.".format(id))
        return 0
    return 1


def getApprovers(gl, cdProject, cdFolder):
    try:
        owners = cdProject.files.raw(file_path=cdFolder+"/OWNERS", ref='master')
        try:
            assignees = [o for o in owners.decode().strip().split('\n')]
            assignee_id = [gl.users.list(username=assignee)[0].id for assignee in assignees]
            return assignee_id
        except IndexError:
            logging.error("OWNERS file is empty")
            return []
    except gitlab.exceptions.GitlabGetError:
        logging.error("OWNERS file is not found.")
        return []
    

def getOldTag(cdProject, repoName):
    try:
        files = cdProject.repository_tree(recursive=True, all=True)
        for file in files:
            if file['type'] == 'blob':
                file_content = cdProject.files.raw(file_path=file['path'], ref='master')
                if repoName in str(file_content):
                    for i in file_content.decode().split('\n'):
                        #if 'image' in i: return i.split(':')[-1].strip()
                        ### Code on Cloud
                        if 'tag' in i:
                            i = re.sub(r'[\n\t ]', '', i)
                            #Oldest i = re.search('(?<=:)(v)?(((\d(\.\d)+)-)?([a-z0-9]+)|[a-z]-)?([a-z0-9]+)',re.sub(r'[\n\t ]', '', i))
                            #Older i = re.search('(?<=:)(v)?(((\d(\.\d)+)-)|[a-z]-)?([a-z0-9]+)',re.sub(r'[\n\t ]', '', i))
                            i = re.search('(?<=:)(m-)?(v)?((\d\.){2}\d-|[a-z]-)?([a-z0-9]+)',re.sub(r'[\n\t ]', '', i))
                            return i.group(0)
        logging.error("Repository [{}] is not found".format(repoName))
        return ''
    except gitlab.exceptions.GitlabGetError:
        logging.error("CD repository is empty or not initialized yet")
    
    

def logConfig(parser):
    logging.basicConfig(filename=parser.get('LOG', 'LOG_PATH')+'/'+parser.get('LOG', 'LOG_FILENAME'), 
                        level=logging.INFO,
                        format='%(asctime)s | %(levelname)s | %(message)s',
                        datefmt='%d/%m/%Y | %I:%M:%S')


def searchFile(cdProject, repoName):
    fileList = []
    files = cdProject.repository_tree(recursive=True, all=True)
    for file in files:
        if file['type'] == 'blob':
            file_content = cdProject.files.raw(file_path=file['path'], ref='master')
            if repoName in str(file_content):
                fileList.append(file['path'])
    return fileList
