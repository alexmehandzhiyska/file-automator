#!/usr/bin/env python3

import os
from shutil import move
import osxmetadata

import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import dirs

def search_main_dirs(tags):
    main_dir_tags = filter(lambda tag: tag in dirs.main.keys(), tags)
    main_dir_tag = list(main_dir_tags)[0]
    return dirs.main[main_dir_tag]

def search_sub_dirs(tags):
    sub_dir_tags = filter(lambda tag: tag in dirs.sub.keys(), tags)
    sub_dir_tag = list(sub_dir_tags)[0]
    return dirs.sub[sub_dir_tag]

def get_file_tags(file):
    try:
        md = osxmetadata.OSXMetaData(f'{dirs.source_dir}/{file.name}')
        tags_objs = md.tags
        tags = []

        for tag in tags_objs:
            tags.append(tag.name)

        return tags
    except:
        return None

def move_file(file):
    tags = get_file_tags(file)
    current_dir = dirs.target_dir_base

    try:
        if tags:
            main_dir = search_main_dirs(tags)
            sub_dir = search_sub_dirs(tags)

            move(file, f'{current_dir}{main_dir}{sub_dir}')
    except:
        pass

class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with os.scandir(dirs.source_dir) as files:
            for file in files:
                move_file(file)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = dirs.source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(20)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()