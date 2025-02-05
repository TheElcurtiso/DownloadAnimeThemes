# Anime Openings and Endings Downloader

`DISCLAIMER: This only works for MAL (MyAnimeList) at the moment! I might look into making it compatible for Anilist
eventually!`

Hi, if you're like me you like anime openings and endings and if you're really like me maybe you've spent a bit too much 
time on [Anime Music Quiz](https://animemusicquiz.com/) and you need that little extra boost to dominate against your 
friends. The thing is its hard to get all that music in one place and I agree! I mean I've seen nearly 200 shows now and 
I can't keep track of everything that's going to come up on AMQ. Well this python script is the answer! Finally, you can 
get all the music to jam to and train on in one convenient place!

## Setup

Now this script is super simple to set up. As I will lay out here:

### Downloading and setting up the repository

First, just clone or download the repository as a ZIP and put it wherever you like in your file explorer (as long as you
can find it!). Open up your terminal and navigate to the folder you put the repo in. Make sure you have [Python](https://www.python.org/downloads/)
installed - it shouldn't matter what version of Python 3 that you use but I'm using `3.12.8` if it makes you feel better.
Now run the following line:

`pip install -r requirements.txt`

that should be all you need to not get any errors when running the python script.

### Running the script

The script takes two command line arguments: the username of the profile on MAL that you want to download the anime themes
of and the client ID from MAL. The username should be clear enough to find - you can use your own or somebody else's it
doesn't matter but the client ID is a bit more tricky as is laid out below:

#### MyAnimeList Account

You need a [MAL](https://myanimelist.net/) account (Sorry Anilist fans!!). Once you've created the account,
you need to click on your user profile in the top right corner and click `Account Settings`. From there, click
the furthest tab to the right labelled `API` then click the `Create ID` button. Its gonna bring you to a form where you
need to write out the app name and type and all that but honestly? You can basically write anything in here (I literally
wrote google.com as my redirect URL 😆) just fill it out and put the app type as `web` and the purpose of use as `hobbyist`.
Once you've submitted that it will bring you back to the page before but now with a shiny `Edit` button below the `Create ID`
button. Just click on the `Edit` button and you should now see a long string of numbers and letters next to Client ID
you just need to copy that (no need for the client secret).

#### Last Steps

You're in the home stretch now! You just need to go back to the terminal and run the script:

`python downloadAnimeThemes.py [INSERT USERNAME] [INSERT CLIENT ID]`

alternatively it could be this if the first doesn't work:

`python3 downloadAnimeThemes.py [INSERT USERNAME] [INSERT CLIENT ID]`

and you're done! It should now start to download all your favourite anime themes!

The songs will be downloaded to a `[USERNAME]-songs` folder in the same place as the original python file.
