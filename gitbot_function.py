import gitlab, configparser, logging, os
from gitbot_module import *

def gitBot(resource, configPath, binPath):
    # Config file module
    parser = configparser.ConfigParser()
    parser.read(configPath)

    # Logging module
    logConfig(parser)

    # Gitlab module
    gl = gitlab.Gitlab(parser.get('GITLAB', 'GITLAB_ADDRESS'), private_token=parser.get('GITLAB', 'GITLAB_TOKEN'))

    # Variables definition
    global workPath, cdProject
    branchName = 'master'
    repoName = resource.split(':')[0]
    newTag = resource.split(':')[1]

    logging.info("Gitbot is proceeding new image [{}]".format(resource))
    env, cdProject = checkEnvironment(gl, parser, newTag)
    if env != '':
        oldTag = getOldTag(cdProject, repoName)
        location = searchFile(cdProject, repoName)
        branch_list = [branch.name for branch in cdProject.branches.list()]

        if env == 'release':
            if newTag in branch_list: 
                logging.warning('Branch [{}] is existing.'.format(newTag))
                cdProject.branches.delete(newTag)
                logging.info('Gitbot has removed old [{}] branch'.format(newTag))
            logging.info('Gitbot is creating a new [{}] branch'.format(newTag))
            cdProject.branches.create({'branch': newTag, 'ref': 'master'})
            branchName = newTag

        if oldTag != '':
            logging.info('GitBot is comparing old tag [{}] to new tag [{}].'.format(oldTag, newTag))
            if (lambda x,y: (x>y)-(x<y))(oldTag,newTag) == 0: logging.info("==> No tag changed!!!")
            else: changeTag(gl, resource, cdProject, oldTag, newTag, binPath, location, branchName)
    else: logging.error("==> The image [{}] is rejected to deploy.".format(resource))
