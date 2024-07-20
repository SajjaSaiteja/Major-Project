Activity Monitoring tool used for tracking or monitoring Employee’s activities within an organization [7]. In Activity monitoring tool we use different types of packages available in python such as logging, pathlib, subprocess, smtplib, sounddevice, shutil, requests, Process, ImageGrab, socket, os, re, time for monitoring Keyboard, Screenshots, Microphone, System and Network information activities from employees, stored as logs in the employee system itself and forwarded these logs to admin Email [8]. After completely sending these logs to admin the logs are automatically deleted.

The following are the methods, approaches to obtain the output [9]: 
1.	First the Activity monitoring tool is installed in the employee system, and admin enters his email and password to get the employee’s activities into his email. 
2.	Then the tool start running on the employee system generates the logs and stored on the employee Desktop/Laptop in the specified path based on the type of files. 
3.	The logs which are generated on the employee system are keyboard, screenshot, microphone, system and network information inputs used for monitoring the employee activities. 
4.	The pressed keys on the keyboard are saved as.txt format in the chosen directory as keylogs. 
5.	Every 15 seconds, a screenshot is taken and saved as a picture in the chosen directory as Screenshots.
6.	Every 10 seconds, the microphone input is recorded and saved as .wav format in the chosen directory as Recording. 
7.	Employee System information are saved as .txt format in the chosen directory as system information. 
8.	Employee network information are saved as .xml format in the chosen directory as network information. 
9.	The files are now aggregated and forwarded to the admin via email based on the file type using regex magic from the chosen directory. 
10.	The tool automatically deletes the all files in the directory and then loops back to the beginning to repeat the procedure..
