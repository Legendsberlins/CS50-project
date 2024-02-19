# **CS50-project**
#### Video: https://youtu.be/L33KbZXHjqc?si=5rueb8PcyJX-UYSJ
#### Description: Implementation of a web application that calculate win, draw and lose percentages.

This web application was implemented using Flask (a python framework) which deals with paths and routes, SQL to keep hold of the database and jinja which is a syntax that implements flask in an HTML file.

The application tells a user their success rate i.e. their win rate, draw rate and defeat rate just by one click. The website can be used by one to track their progress in anything (sports, games and even experiments). For example, lets say you are playing a game of chess with a mate and you win the first round, you simply click win and it will appear on screen that you have a 100% record. Then, lets say you lose the next game. It will appear that your win rate has dropped to 50%, your defeat rate has risen to 50% and your draw rate remains 0%.

Due to the reduced complexity of the website, the user is only prompted for a username, password and password confirmation upon registration. Each user has to have a different username and each password has to consist of at least 8 letters, atleast one number and atleast one special character. All of this is stored (passwords encrypted) in a database along with the date and time registered. Upon successful registration, the user is prompted to the index page [index page](https://super-trout-v457j69prxpf4q6-5000.app.github.dev/) which is where the main process occurs.

I am happy that I managed to develop this and hope it comes to use everywhere around the world but it would not have been possible without the knowledge of Prof. David Malan and his team at Havard CS50. This was CS50.

