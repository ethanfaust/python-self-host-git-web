#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>

#include <git2.h>

#define MAX_PATH 255

// your filesystem path here
const char *git_root = "/git";

static void create_initial_commit(git_repository *repo) {
  git_signature *sig;
  git_index *index;
  git_oid tree_id, commit_id;
  git_tree *tree;
  
  if (git_signature_now(&sig, "Git Infrastructure", "git@domain.example") < 0) {
    fprintf(stderr, "Unable to create a commit signature.\n"
                    "Perhaps 'user.name' and 'user.email' are not set\n");
    exit(1);
  }

  if (git_repository_index(&index, repo) < 0) {
    fprintf(stderr, "Could not open repository index\n");
    exit(1);
  }

  if (git_index_write_tree(&tree_id, index) < 0) {
    fprintf(stderr, "Unable to write initial tree from index\n");
    exit(1);
  }
  git_index_free(index);

  if (git_tree_lookup(&tree, repo, &tree_id) < 0) {
    fprintf(stderr, "Could not look up initial tree\n");
    exit(1);
  }

  if (git_commit_create_v(&commit_id, repo, "HEAD", sig, sig,
                          NULL, "initial (blank) commit", tree, 0) < 0) {
    fprintf(stderr, "Could not create initial commit\n");
    exit(1);
  }
  git_tree_free(tree);
  git_signature_free(sig);
}

int main(int argc, char **argv) {
  //printf("uid: %d; euid: %d\n", getuid(), geteuid());
  //printf("gid: %d; egid: %d\n", getgid(), getegid());  

  if (argc != 2) {
    fprintf(stderr, "Usage: %s reponame\n", argv[0]);
    return 1;
  }

  char *repo_name = argv[1];
  for (int i = 0; i < MAX_PATH; i++) {
    if (repo_name[i] == 0) {
      break;
    }
    if (isalnum(repo_name[i]) ||
        repo_name[i] == '_' ||
        repo_name[i] == '-') {
      continue;
    }
    fprintf(stderr, "Invalid character in reponame\n");
    return 1;
  }

  char path[MAX_PATH];
  int result = snprintf(path, MAX_PATH, "%s/%s.git", git_root, repo_name);
  if (result > MAX_PATH) {
    fprintf(stderr, "Too many characters in reponame\n");
    return 1;
  }

  umask(0);
  if (mkdir(path, 0770)) {
    fprintf(stderr, "Failed to create directory\n");
    return 1;
  }

  git_repository *repo;
  git_repository_init_options opts = GIT_REPOSITORY_INIT_OPTIONS_INIT;
  opts.flags |= GIT_REPOSITORY_INIT_BARE;
  opts.mode = 0770;

  // git init --bare
  int err = git_repository_init_ext(&repo, path, &opts);
  if (err < 0) {
    fprintf(stderr, "Failed to initialize git repository.\n");
    const git_error *err = giterr_last();
    fprintf(stderr, "%s\n", err->message);
    return 1;
  }

  // create empty initial commit
  create_initial_commit(repo);

  return 0;
}
