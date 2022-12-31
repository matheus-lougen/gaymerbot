
# GaymerBOT
A moderation and utility bot that runs on discord

## Running

*I would prefer you don't run an instance of my bot, just join my server to use it, the code is open-source for educational purposes.*

Nevertheless, the installation steps are as follows:
1.  **Some things to know before running**

The project was developed on a Linux environment and it's highly recommended that you run it on the same.
Make sure you have Python3.11 or higher installed and [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) installed via pip, you can install it using `$ python3.11 -m pip install --user virtualenv`

2.  **Clone this repository to your machine**

Run `$ git clone -b production https://github.com/SystemFalll/gaymerbot` to get the production version (recommended).

Run `$ git clone -b development https://github.com/SystemFalll/gaymerbot` to get the development version (not recommended, you can find many unwanted bugs).

3.  **Setup venv**

Access the project folder if you haven't already `$ cd gaymerbot`
Then just do  `$ python3.11 -m virtualenv venv`

4.  **Install dependencies**

Clone [discord.py](https://github.com/Rapptz/discord.py) using `$ git clone https://github.com/Rapptz/discord.py`
Activate the virtual enviroment by running `$ source venv/bin/activate`
Install the discord.py library `$ cd discord.py && python3.11 -m pip install .[voice] -r requirements.txt`
Then go back to the project file `$ cd ..` and run  `$ python3.11 -m pip install -r requirements.txt`

4.  **Create data files**

Run `$ mkdir data && mkdir data/logs && touch data/config.yaml`
See *base_config.yaml* for a basic config structure

5.  **Launching the bot**

Finally run the bot using `$ python3.11 launcher.py [--options]`
Options:
	`--debug`  launch with debug mode.
	`--help`  Show help message.

## Privacy Policy and Terms of Service

Discord requires me to make one of these.

There isn't really anything to note. No personal data is stored.

## License

MIT License

Copyright (c) 2022 Matheus Henrique Lougen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
