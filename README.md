# salior_searching_game
The game uses the "bayes theorem" to search for a survivor

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)

* [Setup & Usage](#setup-&-usage)
* [Project Status](#project-status)

* [Contact](#contact)


## General Information
You are the commander of a search and rescue operation conducted by the Coast Guard. Your task is to find a shipwrecked sailor. The position of the sailor is random, but the last known coordinates are available. The sailor is well-equipped and can survive at sea for three days. You can send two independent search teams per day. The probability of finding the sailor in a given area is based on the sea currents and is as follows:

    Area 1: 0.2
    Area 2: 0.5
    Area 3: 0.3
After each search, the probability of the sailor being in a particular area changes. The efficiency of a single search is random and depends on factors such as weather, and falls within the range of 0.2 to 0.9. Don't waste time, as lives are at stake!

The game utilizes Bayes' theorem to update the probabilities of the sailor being in each area after each search
> More about sea https://en.wikipedia.org/wiki/Bayes%27_theorem


## Technologies Used
 - numpy==1.24.1
 - opencv-contrib-python==4.7.0.68


## Setup & Usage
To start game write in cmd: 
```py main.py```



## Project Status
The Project is in progress. I will try to add some new features in the future.

## Contact
Created by micwoszk@wp.pl - feel free to contact me!
