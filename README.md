if `IN_MOVED_TO`: 
- check the last `IN_MOVED_FROM`. 
    - If it matches, move the file.
    - If it doesn't match, delete the last `IN_MOVED_FROM`
    - If there is no last `IN_MOVED_FROM`, start the transcode

if `IN_MOVED_FROM`: 
- if last `IN_MOVED_FROM` still exists, remove it
- Set last `IN_MOVED_FROM`

if `IN_CREATE`: 
- Register it
- Wait for `IN_CLOSE_WRITE` of the thing

if `IN_DELETE`:
- remove it