# GaymerBOT
A moderation and utility bot that runs on discord

## Running

*I would prefer you don't run an instance of my bot, just join my server to use it, the code is open-source for educational purposes.*

Nevertheless, the installation steps are as follows:
1.  **Some things to know before running**

The project was developed on a Linux environment and it's highly recommended that you run it on the same.
Make sure you have Python3.10 or higher installed and [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) installed via pip, you can install using `$ pip install --user virtualenv`.

2.  **Clone this repository to your machine**

Run `$ git clone -b production https://github.com/SystemFalll/gaymerbot` to get the production version (recommended).

Run `$ git clone -b development https://github.com/SystemFalll/gaymerbot` to get the development version (not recommended, because you can find many unwanted bugs).

3.  **Setup venv**

Access the project folder if you haven't already `$ cd gaymerbot` 
Then just do  `$ python3.10 -m virtualenv venv`

4.  **Install dependencies**

Clone [discord.py](https://github.com/Rapptz/discord.py) using `$ git clone https://github.com/Rapptz/discord.py`
Activate the venv by running `$ source venv/bin/activate`
Install the discord.py library `$ cd discord.py && pip install .[voice] -r requirements.txt`
Then go back to the project file `$ cd ..` and run  `$ pip install -r requirements.txt`

4.  **Create data files**

Run `$ mkdir data && mkdir data/logs && touch data/config.yaml`
See *base_config.yaml* for a basic config structure

5.  **launching the bot**

Finally run the bot using `$ python3.10 launcher.py -debug {True/False}`


## Privacy Policy and Terms of Service

Discord requires me to make one of these.

There isn't really anything to note. No personal data is stored.