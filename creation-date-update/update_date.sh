echo

NUM_FILES="$#"
echo "Number of files to update: ${NUM_FILES}"

for file in "$@"; do
    # echo
    # echo "Working on file: "${file}""

    created_time=$(GetFileInfo -d "${file}")
    # echo "Old created time is: ${created_time}"

    modified_time=$(GetFileInfo -m "${file}")
    # echo "Old modified time is: ${modified_time}"

    SetFile -d "${modified_time}" "${file}"

    created_time=$(GetFileInfo -d "${file}")
    # echo "New created time is: ${created_time}"

    modified_time=$(GetFileInfo -m "${file}")
    # echo "New modified time is: ${modified_time}"
done

echo "Update completed"
echo
