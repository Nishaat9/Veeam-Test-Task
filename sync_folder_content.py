import datetime
import logging
import os
import time
import shutil
import numpy as np
import platform
import sys
from argparse import ArgumentParser

# creating a parser object to add arguments to be use to retrieve in-line arguments
parser = ArgumentParser(description="Synchronize folder contents from Source folder to Replica folder")
parser.add_argument("--source_path", type=str, help="Source Path")
parser.add_argument("--replica_path", type=str, help="Replica Path which needs to be in sync with source path")
parser.add_argument("--log_path", type=str, help="Log path")
parser.add_argument("--interval", type=int, default=10,
                    help="interval in seconds")

# following is created to access the in-line argument values
opt = parser.parse_args()


def remove_files(replica_path, remove_file_ls):
    """
     this method removes files from the replica folder path which are not available in source folder path
     @param replica_path: string containing replica folder path where source folder path files are to be copied
     @param remove_file_ls : list containing files/folders not available in replica folder path.
     @return: none
    """
    for file in os.listdir(replica_path):
        if file in remove_file_ls:
            del_path = os.path.join(replica_path, os.path.basename(file))
            if os.path.isdir(del_path):
                os.rmdir(del_path)
            else:
                os.remove(del_path)


def get_files_to_copy(source_path, replica_path):
    """
     this method creates list of file that needs to be copied
     @param source_path: string containing source folder path
     @param replica_path: string containing replica folder path
     @return: list containing files to be copied
    """
    copy_files_ls = []
    source_files_ls = os.listdir(source_path)
    replica_files_ls = os.listdir(replica_path)

    missing_files_ls = list(np.setdiff1d(source_files_ls, replica_files_ls))
    copy_files_ls = copy_files_ls + missing_files_ls

    existing_file_ls = np.intersect1d(source_files_ls, replica_files_ls)
    for file in existing_file_ls:
        source_time_stamp = os.path.getmtime(os.path.join(source_path, file))
        replica_time_stamp = os.path.getmtime(os.path.join(replica_path, file))
        if source_time_stamp != replica_time_stamp:
            copy_files_ls.append(file)
    return copy_files_ls


def copy_files(source_path, copy_files_ls, replica_path):
    """
     this method copies files from the source folder path to replica folder
     @param source_path: string containing source folder path
     @param copy_files_ls: list containing files to be copied
     @param replica_path: string containing replica folder path
     @return:
    """
    for file in os.listdir(source_path):
        if file in copy_files_ls:
            src = os.path.join(source_path, os.path.basename(file))
            if os.path.isdir(src):
                if os.path.exists(os.path.join(replica_path, os.path.basename(file))):
                    os.rmdir(os.path.join(replica_path, os.path.basename(file)))
                shutil.copytree(src, os.path.join(replica_path, os.path.basename(file)))
            else:
                shutil.copy2(src, replica_path)


def sync_replica_with_source(source_path, replica_path):
    """
    This method implements one-directional synchronizing from source folder to replica folder
    @param source_path: a string containing source folder path
    @param replica_path: a string containing replica folder path where source path files to be copied
    @return:
    """
    source_files = os.listdir(source_path)
    replica_files = os.listdir(replica_path)
    remove_files_ls = np.setdiff1d(replica_files, source_files)
    copy_files_ls = get_files_to_copy(source_path, replica_path)

    if len(remove_files_ls) > 0:
        # following removes the files from replica folder that are not there in source path
        logging.info(
            f'Removing files {remove_files_ls} from replica folder location: {replica_path} at {datetime.datetime.now().strftime("%Y-%m-%d_%H.%M")} as it does not exist in source folder location: {source_path}')
        remove_files(replica_path, remove_files_ls)
        logging.info(f'Removed at {datetime.datetime.now().strftime("%Y-%m-%d_%H.%M")}!!!')

    if len(copy_files_ls) > 0:
        logging.info(
            f'Copying files {copy_files_ls} from source folder location {source_path} at {datetime.datetime.now().strftime("%Y-%m-%d_%H.%M")} to replica folder location {replica_path}')

        # following copies the files from source folder to the replica foler
        copy_files(source_path, copy_files_ls, replica_path)
        logging.info(f'copied at {datetime.datetime.now().strftime("%Y-%m-%d_%H.%M")}!!!')
    return


if __name__ == '__main__':
    source_path = opt.source_path
    replica_path = opt.replica_path
    log_folder = opt.log_path
    sync_interval = opt.interval

    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    log_file_name = 'logfiles_' + datetime.datetime.now().strftime("%Y-%m-%d_%H.%M") + '.log'
    log_file_path = os.path.join(log_folder, log_file_name)
    logging.basicConfig(
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=log_file_path)
    logging.getLogger()

    # following logs the actions to the console
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    if os.path.exists(source_path):
        if os.path.exists(replica_path):
            while True:
                sync_replica_with_source(source_path, replica_path)
                # sleeps for the interval given
                time.sleep(sync_interval)
        else:
            logging.info(f"Replica path {replica_path} does not exist. Please check the path.")
    else:
        logging.info(f"Source path {source_path} not found. Please check the path.")
