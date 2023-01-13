# Veeam-Test-Task
## Problem Statement:
A program needs to be developed in one of the following languages: Python, C/C++, C# that synchronizes the folder contents uni-directionally from Source to Replica folder. Contents from Source folder to replica folder are to be in sync. Synchronization to be performed in regular intervals. Files actions (creation/copying/removal) are to be logged in a file and are to be displayed in console output. Folder paths, synchronization interval and log file path to be passed as command line arguments. 

## Test Cases:
There are 4 cases considered for testing:

a. Check if the Source folder path and the replica folder path exists

b. Files are available in the Source folder but not in Replica folder
 - File are copied to replica folder from Source folder

c. Files are available in Replica folder but removed from Source folder
 - Files from replica folder are removed based on Source folder. Log is created for the removed files in log folder and in console

d. File exists in both Source folder and in Replica folder with version difference 
- File versions are synced in replica folder based upon source folder file

## Approach:
The program is developed with Python
1. Importing modules/libraries to work with several functionalities.
2. Created a parser object that retrieves in-line arguments i.e., source path, replica path,
log file path, and sync interval (in seconds)
3. Created a logging object that log actions such as creation/copying/removal to the log file
as well as displayed in console output
4. Checked if source, replica & log file path exists. In case, source & replica path do not
exist, the program is ended. If log file path does not exist, the program creates a log
folder path
5. Created a while loop to that runs in regular interval (i.e., sync interval passed as an in-line
argument)
6. Created a method ‘sync_replica_with_source’ which implements the three test cases
mentioned above to implement one-directional synchronization from source to replica
folder
7. An example command to run the program is as follows:
a. python sync_folder_content.py –source_path “C:/source/folder/path” – replica_path “C:/replica/folder/path” –log_path “C:/log/folder/path” –interval 300
8. The following flowchart lays out the program flow:
   
<img width="473" alt="image" src="https://user-images.githubusercontent.com/122571916/212187202-8e5093a6-5140-488b-a3ad-c5c60795ff8e.png">



  
