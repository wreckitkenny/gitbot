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
            if env in branch_list: 
                logging.warning('Branch [{}] is existing on Production.'.format(env))
                cdProject.branches.delete(env)
                logging.info('Gitbot has removed old [{}] branch'.format(env))
            logging.info('Gitbot is creating a new [{}] branch'.format(env))
            cdProject.branches.create({'branch': env, 'ref': 'master'})
            branchName = env

        if oldTag != '':
            logging.info('GitBot is comparing old tag [{}] to new tag [{}].'.format(oldTag, newTag))
            if (lambda x,y: (x>y)-(x<y))(oldTag,newTag) == 0: logging.info("==> No tag changed!!!")
            changeTag(gl, cdProject, oldTag, newTag, binPath, location, branchName)
    else: logging.error("==> The image [{}] is rejected to deploy.".format(resource))
