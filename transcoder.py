import inotify.adapters
import os
import shutil
import re
import ffmpeg

def main():
    original_folder = "/home/jeremy/transcoder/original"
    new_folder = "/home/jeremy/transcoder/new"

    i = inotify.adapters.InotifyTree(original_folder)

    last_moved_from = ""
    staged_last_for_rm = False
    created_files = {}

    for event in i.event_gen():

        if event == None:
            if last_moved_from != "":
                staged_last_for_rm = True
                continue
        else:
            (_, type_names, path, filename) = event

            if filename != "":
                print(event)
                fullpath = path + "/" + filename

                if "IN_DELETE" in type_names:
                    remove(original_folder, new_folder, fullpath)
                # add new files
                elif "IN_CREATE" in type_names:
                    created_files[fullpath] = True
                elif "IN_CLOSE_WRITE" in type_names:
                    if created_files[fullpath]:
                        new_path = re.sub("[^\.]+$", "mp3", fullpath.replace(original_folder, new_folder))
                        transcode(fullpath, new_path)
                        del created_files[fullpath]
                # moved out
                elif "IN_MOVED_FROM" in type_names:
                    last_moved_from = fullpath
                # moved in
                elif "IN_MOVED_TO" in type_names:
                    curr_filename = re.search("[^\\/]+$", fullpath).group()
                    try:
                        prev_filename = re.search("[^\\/]+$", last_moved_from).group()
                    except:
                        prev_filename = ""

                    if curr_filename == prev_filename:
                        try:
                            os.makedirs(re.sub("/[^\\/]+$", "", fullpath.replace(original_folder, new_folder)))
                            os.rename(re.sub("[^\.]+$", "mp3", last_moved_from.replace(original_folder, new_folder)), re.sub("[^\.]+$", "mp3", fullpath.replace(original_folder, new_folder))) # move file
                        except OSError as e:
                            print(e)
                        finally:
                            last_moved_from = ""
                            staged_last_for_rm = False
                    else:
                        new_path = re.sub("[^\.]+$", "mp3", fullpath.replace(original_folder, new_folder))
                        transcode(fullpath, new_path)

        if staged_last_for_rm:
            remove(original_folder, new_folder, last_moved_from)

def transcode(original_path, new_path):
    (
        ffmpeg
        .input(original_path)
        .output(new_path, audio_bitrate="256k")
        .overwrite_output()
        .run()
    )

def remove(original_folder, new_folder, path):
    try:
        if os.path.isdir(path.replace(original_folder, new_folder)):
            shutil.rmtree(path.replace(original_folder, new_folder))
        else:
            if os.path.exists(re.sub("[^\.]+$", "mp3", path.replace(original_folder, new_folder))):
                os.remove(re.sub("[^\.]+$", "mp3", path.replace(original_folder, new_folder)))
    except OSError as e:
        print(e)

if __name__ == '__main__':
    main()