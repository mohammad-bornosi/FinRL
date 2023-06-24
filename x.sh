git filter-branch --prune-empty -d /dev/shm/scratch \
--index-filter "git rm --cached -f --ignore-unmatch train.parquet" \
--tag-name-filter cat -- --all