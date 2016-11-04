# proj6-mongo
Simple list of dated memos kept in MongoDB database
Author: Elijah Caluya

## What the repository started with

A simple Flask app that displays all the dated memos it finds in a MongoDB database.
There is also a 'scaffolding' program, db_trial.py, for inserting a couple records into the database 
and printing them out.  

## Assignment

For the database, I needed to create an admin account with my own password and username.
For any of the other clients who want to use the database, I created a file that contains 
the needed information for a user that I created the username and password for.

- secrets/admin_secrets.py holds configuration information for my MongoDB
  database, including the administrative password.  
= secrets/client_secrets.py holds configuration information for my
  application. 



## Functionality added

The user is able to create memos from the entry fields at the bottom of the page.
The memos are then presented in date order and the user is able to delete the selected
memos.

## Setting up

Our use of the database is pretty simple, but you should anticipate
that installing MongoDB could take some time.  Since you may not be
able to install the same version of MongoDB on your development
computer and your Pi, it will be especially important to test your
project on the Pi. 

The version of MongoDB available for installing on Raspberry Pi with
apt-get is 2.4.  The version you can find for your development
computer is probably 3.x.  You may even have difficulty finding
documentation for 2.4, as it is considered obsolete.  However,
commands that work for 2.4 still seem to work for 3.x, so you should
write your application and support scripts to use 2.4.   The
difference that may cause you the most headaches is in creating
database user accounts (which are different than the Unix accounts for
users). 

In Python, the pymongo API works with both versions of MongoDB, so
it's only the initial setup where you have to be  
careful to use the right version-specific commands. 


