# Project Title
Muziqer - personal music storage

## Author
Author: Jonasz Adamski - CS50’s Introduction to Computer Science online student
GitHub: [YonashA](https://github.com/YonashA)
ID: YonashA
edX Account: jonasz_a
Country: Poland
City: Krakow
Year: 2022

## All about the Project
### Description:
Muziqer is a web app to keep records of all music CDs, DVDs, pieces of vinyl, etc. owned by the user.
Keep track of your music portfolio, stored in one place, with easy online access, with a simple UI allowing quickly to add or remove labels, filtered and sorted as needed.

Inspired by my father-in-law, who is a great melomaniac with a large number of music records on different mediums, stored on several shelves in his house. That pushed me to create this app to help him classify all his music records, with an easy UI and available online, to allow finally to ditch old, full of errors Excel files.

### Video Demo:
Video about the project and overview of use.
URL: <https://youtu.be/UwLX81c35-U>

### Tech used:
* Python
* Flask
* Bootstrap
* JavaScript & jQuery
* SQL

Flask seems to be very good for smaller projects written in Python, which includes sqlite database - a lighter db is more than enough for the type of Project. Used several scripts to improve UI/UX and reduce the number of HTML pages (for example one page for login & registering) - with a combination of pure JavaScript and jQuery.

### Features:
Muziqer app with the current version contains below features:
* User's registration with validation
* User's login and log out
* Dummy forgot/reset password functionality
* Home ("Portfolio") site with a table of all records in the database, with search, sorting, filtering, and pagination functionality using JS/jQuery
* Availability to remove records with one click directly from the portfolio table
* Adding new records ("Add") to the database, with improved UX functionality (search list of all music genres when typing) and validation (required fields)
* Live stats of the number of records, number of music mediums, and last time the database was updated
* Dummy contact form to send a message to the admin
* Floating navbar only when logged in
* Footer fixed to the bottom of page
* Easy UI, improved UX
* "Back to top" button using jQuery to quickly move to the top of the page

### Future features:
A list of ideas to implement in further versions:
+ Allow user to delete their account and remove all records
+ Allow user to remove all records in bulk
+ More validations for duplicate records (taking into consideration, artists can have multiple albums, different artists can have the same names of albums, and user typing album name can make errors that won't be caught by the validation)
+ Connect API to fetch more music metadata (and be used as 'search' functionality to add albums without typing errors and duplicates)
+ Add Info section about each album, where the user can enter and read more details about the album (from API), including albums covers (image)
+ When live, link with email SMTP
+ When live, add Flask-secured authorization for user registration
+ When live, real password forget/reset functionality
+ When live, working contact form
+ Possibility to download user's database to Excel/CSV/PDF
+ Further JS/JQuery improvements

Implementation of the above features will require some more knowledge of Flask functionality, advanced API connections, and more practice with JS/jQuery. Finally, more research around the live implementation of the Flask web app.

### Dependencies
* cs50
* Flask
* Flask-Session
* requests
* Bootstrap 5
* Werkzeug
* datetime
* jQuery and JS scripts

### Executing program
* How to run the program:
```
flask run
```
* Register new user and start adding new records
* There are several users already registerd with large music records stored in database (ids to test via sqlite commands are: 1, 2, 3). Run db in terminal:
```
sqlite3 muziqer.db

```
and use SQL code to access dummy data:
```
SELECT * FROM users WHERE id = 1;

```
* Other databases available (ie. "genres", "records"), run in sqlite3:
```
.schema

```

### Help
Any questions or issues.
Message me via Github: [YonashA](https://github.com/YonashA)

### Version History
* 0.1
    * Initial Release as a Final Project for CS50’s Introduction to Computer Science (December 2022)

## Thank you
Special thanks to the CS50 Team at Harvard for a great journey and an amazing course, inspiring lectures, and interesting problems!