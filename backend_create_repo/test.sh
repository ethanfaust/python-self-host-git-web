#!/bin/bash

GIT_ROOT=/git
TEST_REPO=foo

rm -rf $GIT_ROOT/$TEST_REPO.git

chown git create_git_repo
chgrp git create_git_repo
chmod 6510 create_git_repo
su efaust -c "id && ./create_git_repo $TEST_REPO"
