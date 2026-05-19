#!/bin/bash

BASE_DIR=$1
ASSIGNMENT=$2
RUN_COUNT=0

echo "Projects: $BASE_DIR"
echo "Assignment: $ASSIGNMENT"

projects=$(ls $BASE_DIR)
count=$(ls -d */ $BASE_DIR | wc -l)
echo "Projects found: $count"
echo "--------------------"
for project in $projects; do
    project_path=$BASE_DIR/$project
    if [ -d "$project_path" ]; then
        printf '%s found \n' $project_path;
    fi
done
echo "--------------------"
echo "running Autofeedback"
for project in $projects; do
    project_path=$BASE_DIR/$project
    if [ -d "$project_path" ]; then
        RUN_COUNT=$(($RUN_COUNT + 1))
        echo "Starting evaluation on $project_path"
        echo "$RUN_COUNT / $count"
        printf "\n\n"
        python -m autofeedback.main $project_path $ASSIGNMENT
    fi
done