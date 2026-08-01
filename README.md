# Musical Insights — Interactive Music Recommender

## Overview
I decided to make a music recommendation application since i listen to music way too much whenever I'm doing any task. It gave me the chance 
to combine come of my computer science related interests and chance to find new songs that I most likely would not have discovered otherwise.
The application can be ran locally through VS code or an alternative IDE.

<img width="944" height="570" alt="image" src="https://github.com/user-attachments/assets/adc52433-84fb-490d-b075-b3b2cecacbab" />


## How it Works
Here's the the data flow of the web application
<img width="1248" height="327" alt="image" src="https://github.com/user-attachments/assets/16858594-ba75-4382-9e20-532cdd9f399a" />

## Curated Matches
To recommend songs I needed to account for genre similarity and the weighted "love rating". This was easier to do with a set amount of songs
in comparison to a list where the number of tracks could be any any given number. The matches give the user the genre, song length and artist 
after performing the match finding process. 

This was an interesting part of the project because I had to consider various scenarios that the user try with the song might look-up 
feature. For example, what if the user picked the same song for all three tracks? Should I just recommend the same song for the five matches?
In that specific case I thought it would be best if the song matches remained unique.

<img width="1021" height="544" alt="image" src="https://github.com/user-attachments/assets/c78ffab2-2d23-4a82-b2af-0c55a33508e8" />


The recommended songs are from artists that are similar in genre at the very least.

<img width="862" height="580" alt="image" src="https://github.com/user-attachments/assets/943fe1ad-0ca2-4af3-bafc-29160c65635c" />


If a song entered in the one of the track searches is not in the data base then user receives an alert.
<img width="348" height="143" alt="image" src="https://github.com/user-attachments/assets/7071b521-ec0b-4da0-9673-0fb47dbba481" />


## Experience
I chose to take on the project because it would be chance to use technologies that I was not too familiar with. I had used HTML and CSS in the past, but it was primarily for my personal portfolio website. The only experience I had with Javascript was in high school for an AP Computer Science class, but once again I had never actually used it for a somewhat long term project. 

For the Database, I really wanted to use Spotify's song API for developers, but it was only available for premium users of Spotify. I decided to settle for a local database that I downloaded from Kaggle that was used in similar song data analysis projects. The downside of this is that I have fewer songs to pool from when searching and recommending songs for users. In the future I'll probbaly use some sort of song API.

Right now, the recommendation engine uses a fixed math formula to find similar tracks. In the future, I want to make the engine modular so you can easily swap between different matching algorithms and compare which one actually picks the best songs for a specific person.

### Pros
* Simple and fairly straight forward User Interface
* Ignores duplicates in curated matches
* The recommendation speed is about ~.500 ms on average
* Avoids looping searches an infinite loop in general
* Searching the local database is relatively fast
* Gracefully alerts users if a track isn't in the database or if server connection issues occur
  
### Cons
* Database does not allow for concurrent inserts
* Only ~85,000 unique songs within the database
* Rarely recommends songs by artists chosen by the user
* The user interface could of more instructions for an even easier first time use case




