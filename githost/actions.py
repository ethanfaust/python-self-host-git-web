import os
import re
import subprocess

from . import config

def iter_repos():
  for repo_name in os.listdir(config.git_root):
    match = re.match(r'([^.].*)[.]git', repo_name)
    if match:
      yield match.group(1)

def create_repo(repo_name):
  p = subprocess.Popen(['create_git_repo', repo_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  out, err = p.communicate()
  err = err.decode('utf-8').strip()
  return p.returncode == 0, err

