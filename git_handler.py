import os
import git
from utils import ensure_directory_exists

def create_git_repo(project_name):
    base_path = os.path.join(os.getcwd(), 'projects')
    ensure_directory_exists(base_path)
    
    repo_path = os.path.join(base_path, project_name)
    ensure_directory_exists(repo_path)
    
    repo = git.Repo.init(repo_path)
    return repo_path

def commit_changes(repo_path, commit_message):
    repo = git.Repo(repo_path)
    repo.git.add(A=True)
    repo.index.commit(commit_message)
