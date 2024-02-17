#!/bin/bash


get_git_info() {
    repository_name=$(basename $(git remote get-url origin) .git)

    repository_url=$(git config --get remote.origin.url)

    branch=$(git rev-parse --abbrev-ref HEAD)

    commit_hash=$(git rev-parse HEAD)

    commit_url="${repository_url%/}.git/commit/$commit_hash"

    author=$(git show -s --format='%an' HEAD)

    date=$(git show -s --format='%ci' HEAD)

    message=$(git show -s --format='%B' HEAD | sed 's/"/\\"/g')
    
    echo "{
    \"Repository\": {
        \"Name\": \"$repository_name\",
        \"URL\": \"$repository_url\"
    },
    \"Branch\": \"$branch\",
    \"Commit\": {
        \"Hash\": \"$commit_hash\",
        \"URL\": \"$commit_url\"
    },
    \"Author\": \"$author\",
    \"Date\": \"$date\",
    \"Message\": \"$message\"
}"
}

get_git_info