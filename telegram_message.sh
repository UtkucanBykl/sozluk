#!/usr/bin/env bash

TOKEN=$TOKEN
CHAT_ID=$CHAT_ID
MESSAGE='Sozluk Commit => '$COMMIT_URL$TRAVIS_COMMIT' Commit Message: '$TRAVIS_COMMIT_MESSAGE' Event Type: '$TRAVIS_EVENT_TYPE' Branch: '$TRAVIS_PULL_REQUEST_BRANCH' Statu:'$STATU
URL="https://api.telegram.org/bot$TOKEN/sendMessage"

curl -s -X POST $URL -d chat_id=$CHAT_ID -d text="$MESSAGE"