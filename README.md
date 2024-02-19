# **Success%:Implementation of a web application that calculate win, draw and lose percentages.**
#### Video: https://youtu.be/L33KbZXHjqc?si=5rueb8PcyJX-UYSJ
#### Description:
This web application was implemented using Flask (a python framework) which deals with paths and routes, SQL to keep hold of the database and jinja which is a syntax that implements flask in an HTML file.

The application tells a user their success rate i.e. their win rate, draw rate and defeat rate just by one click. The website can be used by one to track their progress in anything (sports, games, and even scientific experiments). For example, let's say you are playing a game of chess with a mate and you win the first round, you simply click win and it will appear on screen that you have a 100% win record, a 0% draw record and a 0% lose record. Then, let's say you lose the next game. It will appear that your win rate has dropped to 50%, your defeat rate has risen to 50% and your draw rate remains 0%. And lastly, let's say there's a tie breaker which still ends up as a tie. Your win rate will drop once more to 33.3%, as well as your lose rate and your draw rate will rise to 33.3%. That is how it works.

Due to the reduced complexity of the website, the user is only prompted for a username, password and password confirmation upon registration. Each user has to have a different username and each password has to consist of at least 8 letters, at least one number and at least one special character. All of this is stored (passwords encrypted) in a database along with the date and time registered. Upon successful registration, the user is prompted to the index page [index page](https://super-trout-v457j69prxpf4q6-5000.app.github.dev/) which is where the main process occurs.

This repository also includes a templates folder which consist of HTML files which help build the interface of what the application looks like. It consists of layout.html which builds the navigation of the software and with the help of jinja syntax combines all other files in the templates folder into one. It also consists of details about the software and has links from bootstrap which have been used to improve its interface.

The index.html file shows the main part of the software i.e. the table which computes the users win rate, draw rate and lose rate and the form which consists of win, lose and draw buttons and increments the Win, Draw and Lose columns in the table corresponding to the button the user clicks.

The register.html file replicates what a registration page should look like consisting of a username, password and a password confirmation input. Remember that as previously stated, two users can't share the same username in the database therefore, if a user inputs a username which is already stored in the database, he/she will be prompted to a "400 error" message.

The login page also replicates what a login page should look like consisting of username and password fields. The username placed in has to be in the database and has to correspond with the encrypted password in the database for the user to be taken to their home page.

The apology.html consists of the image and error message which will appear if the user inputs an invalid password, logs in with a name not stored in the database, registers with a username already in the database and whatnot.

Outside the templates folder, the app.py file is the complete backbone of this repository and software. It is where all the backend code and logic run. It consists of flask, sql code.

The repository also consists of files like helpers.py which implements some of the functions used from back to front, register.db which is where the database is kept. This database consists of two tables (registrants and records). The registrants table takes record of all registrants of the software while the records table tracks users percentage records.

There's certainly room for improvement and several updates are already look upon at like the implementation of a 'clear' button, a better interface and so on.

I am proud to have managed to develop this and hope it comes to use everywhere around the world as I know the potntial of such a web application if the right ideas are implemented. Lastly, this would not have been possible without the knowledge of Prof. David Malan and his team at Havard CS50 (Mr. Carter Zenke, Mr. Doug Lloyd, Mr. Brian Yu) and many others who play such a big role behind the scenes. Thank you for everything. This was CS50.

