**<h1 align="center">University Discord Bot</h1>**

<div align="center">

[**About**](#about)

[**Setup Requirements**](#setup-requirements)

[**Getting Started**](#getting-started)

[**How to setup a Raspberry Pi for the bot**](#how-to-setup-a-raspberry-pi-for-the-bot)

[**Contributing To This Repo**](#contributing-to-this-repo)
<br><br>

</div>

# About

This Discord bot was created to assist class representatives and moderators with the management of channels and projects. It can be fully customised by implementing the full extent of the API features found at the link below. The commands below are currently implemented; however, this may change in the future.

<details>
<summary>Commands Index</summary>
<br>

#### SHUTDOWN

`!EEE SHUTDOWN`

This command is reserved for admins only and can be
used to shutdown the bot from the discord client.

#### AddCourse

`!EEE AddCourse <Course Code> <1,2,3,4> <EE,ECE,MTRX,CSC> <elective-Y-N>`

This command can be used to add a course with specific
course streams and years or even an elective. The command is reserved
for use by admins and class reps.

#### DeleteCourse

`!EEE DeleteCourse <Course Code> <1,2,3,4>`

This command can be used to delete a specified
course. The command is reserved for use by
admins and class reps.

#### ArchiveCourse

`!EEE ArchiveCourse <Course Code> <1,2,3,4>`

This command can be used to archive a specified course
to the archive category. The command is reserved for use by
admins and class reps.

#### AddProject

`!EEE AddProject <project-name-with-dashes> "<short description in quotes>"`

This command can be used to request a set of new channels
related to a project of your choosing. The command can be used by any member
of the server. **(NOTE: approval by the class admins is needed before the
channel is created)**

#### DeleteThisProject

`!EEE DeleteThisProject <reason without quotes>`

This command can be used to delete a specified
project and requires a reason. The command may be used
by any member of the server.

#### ArchiveThisProject

`!EEE ArchiveThisProject <reason without quotes>`

This command can be used to archive a specified
project and requires a reason. The command may be used
by any member of the server. Archived projects can be retrieved
by contacting the server admins or class reps.

#### ClearChannel

`!EEE ClearChannel`

This command is reserved for admins only and can be
used to clear entire text channels. **_(NB! This is a
destructive action and cannot be undone!)_**

#### Play

`/play | $play | +play | &play`

Music bot commands

#### ClearMusic

`!EEE ClearMusic`

Use this to clear the music channel of all messages.

</details>
<br>

# Setup Requirements

You will need to ensure that you have done the following before cloning the repository:

- Installed Python 3.7 or later
- `pip` must be updated to the latest version
- Read the `discord.py` [API documentation](https://discordpy.readthedocs.io/en/latest/api.html)
- Optional: if you're using a Raspberry Pi, ensure that your OS is up to date by running `sudo update` and then `sudo upgrade`<br><br>

# Getting Started

Here's how to get started with your own University Discord Bot project!

## **Step 1:**

Clone this repository to your computer to get started by using the following git command in your command line:<br>
`git clone https://github.com/ryxcam002/UniDiscordBot`<br>

## **Step 2:**

Change directory into the newly cloned repo using:<br>
`cd UniDiscordBot`<br>

## **Step 3:**

Open a terminal and run `pip install -r requirements.txt`

If you're using linux you may need to use `sudo` to install these packages.

(Note: This bot has been tested on a Raspberry Pi and you will need to use `sudo su` and then install the above packages. This will allow you to run the python script on startup. See [this section]() on how to set this up)<br>

## **Step 4:**

Finally, run the python script called `main.py` once you have changed directory into the UniDiscordBot folder. This can be done in the following way:

Windows CMD: `python3 main.py`

Linux Terminal: `sudo python3 main.py` <br><br>

# How to setup a Raspberry Pi for the bot

## **Step 1:**

Open a terminal window and run the following command to edit your `rc.local` file:

`sudo nano /etc/rc.local`

## **Step 2:**

Once the file is open, add the following line of code just before the last line which reads `exit 0`:

`sudo python3 /home/pi/UniDiscordBot/main.py &`

(The '&' will ensure that your bot runs in the background)

## **Step 3:**

Next you will need to install the python package requirements for the bot at the root level. Run:

`sudo su`

You may need to supply the root password for the command above. Once this has been done, navigate to the UniDiscordBot directory (this may vary from below if you cloned the repo elsewhere) and install the requirements:

`cd /home/pi/UniDiscordBot`
`pip install -r requirements.txt`

## **Step 3:**

Next you will need to setup the Raspberry Pi to run in headerless mode (no GUI desktop will be shown). To do this run:

`sudo raspi-config`

Select the 'Boot Options' menu item, then the option which reads 'Console Autologin'. Finally, reboot the Pi when it asks you to do so or run `sudo reboot`. The bot will now autolaunch every time the Pi starts.

# Contributing To This Repo

- [x] To begin contributing, request permission from the repo owner to begin collaborating.
- [x] Clone the repo and add new features and share them with your friends
- [x] Create issues for any bugs you might find
