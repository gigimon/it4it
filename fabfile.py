from fabric.api import *
import fabric.contrib.project as project
import os

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'site'
env.preview_path = 'preview'
DEPLOY_PATH = env.deploy_path

# Remote server configuration
production = 'root@it4it.ru:22'
dest_path = '/var/www/it4it.ru'


def clean():
    if os.path.isdir(DEPLOY_PATH):
        local('rm -rf {deploy_path}'.format(**env))
        local('mkdir {deploy_path}'.format(**env))
    if os.path.isdir(env.preview_path):
        local('rm -rf {preview_path}'.format(**env))
        local('mkdir {preview_path}'.format(**env))

def build():
    local('pelican -s publishconf.py')

def rebuild():
    clean()
    build()

def regenerate():
    local('pelican -r -s publishconf.py')

def serve():
    local('cd {preview_path} && python -m SimpleHTTPServer'.format(**env))

def reserve():
    build()
    serve()

def preview():
    local('pelican -s previewconf.py')
    local('cd {preview_path} && python -m SimpleHTTPServer'.format(**env))    


@hosts(production)
def publish():
    local('pelican -s publishconf.py')
    project.rsync_project(
        remote_dir=dest_path,
        exclude=".DS_Store",
        local_dir=DEPLOY_PATH.rstrip('/') + '/',
        delete=True
    )
