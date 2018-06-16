REPUTATION BASED TRUST EVALUATION IN E-COMMERCE APPLICATIONS AND CHATBOT

What is it?

A web application that fetch the review from the shopping site i.e Amazon and displays the overall rating of the particular product. Here, the reviews of the Amazon’s product are fetched into the database and uses naive bayes algorithm to classify the reviews into positive and negative and displays the result in the form of pie chart. It also provides a ChatBot support for the communication facility with the customer.

Software Requirements

•	Operating System : Windows (Windows 10), Ubuntu 16

•	Language : Python 3.1+ version

•	Algorithm : Naive Bayes

•	Database: SQLite 3

•	IDE: Pycharm

•	Web Frame Work: Django

•	Packages: requests, dateutil, bs, beatifulSoup4, urllib, validators, lxml, nltk, time, re, channels, string, bcrypt, json, csv, os.

Hardware Requirements

•	RAM : 1 GB and More

•	Processor : Intel Celeron or higher

•	Monitor : 15’’ Color

•	Hard Disk : 40 GB

•	Speed : 1GHZ and more

•	Mouse : Wired or Wireless

•	Keyboard : Wired or Wireless

Before Debugging

•	You need to have preinstalled Pycharm IDE and Python 3 on your OS.

•	Check the System Requirements Specification and install the required packages.

•	Internet Connection is required to fetch the reviews from Amazon server for required product and to display the pie chart.

Debugging

•	Open Pycharm IDE.

•	Click on File and select Open and click on it.

•	A new Open window pops up on the screen.

•	You can select amazon project and select open selected.

•	Amazon project opens up on the Pycharm IDE.

•	You can click on View->Tool Windows->Terminal

•	Terminal opens up at the bottom.

•	Use cd and dir command to locate the manage.py file and its associated directory.

•	Once the directory of manage.py is known, you can proceed further.

•	Type the command as python manage.py migrate --run-syncdb

•	After the successful execution of this command. You can proceed further.

•	Type the command as python manage.py runserver

•	Open a Web Browser and type http://127.0.0.1:8000/ as a link and click enter.

•	A login and register page appears on the screen.

•	Enter the First Name, Last Name, Email, Password, Confirm Password in the required field and click on Register button.

•	On the successful registration, successful screen appears up.

•	Customer can click on Log out button to log off from the services.

•	Later when the customer needs access to the amazon sentiment analysis service. He can use the same email and password to login through the login page and successful page appears up on the successful login.

•	Customer can enter Product name in the text box assigned to it and click on submit. Eg.: Mobile

•	A list of Product appears up on the screen below product index.

•	Customer can select one product from the list by entering the index. Eg.: 2

•	Customer can now click on any button now i.e, Few Product Reviews, Sentiment Analysis Based on Reviewsand Overall Rating or ChatBot Support.

•	By clicking on Few Product Reviews, customer gets information regarding reviews about the selected product with product link and price.

•	Customer can click on Try Another Product button to get back to previous screen to try out other product or to use the services of another button.

•	Customer can click on Sentiment Analysis Based on Reviews and Overall Ratings button to get the sentiment of the reviews regarding the selected product.

•	Overall ratings of the selected product is displayed on the screen, in terms of percentages assigned for *, **, ***, **** and *****.

•	Customer can click on submit button inside the Sentiment Analysis page to get the sentiment of the reviews regarding the selected product. It can be either positive or negative.

•	Customer can enter the review in text box which is at the top of the page to get the sentiment about the selected reviews after clicking on submit button.

•	Customer can click on Try Another Product button to get back to previous screen to try out other product or to use the services of another button.

•	Customer can click on ChatBot Support button for customer interaction with the bot. 

•	Bot can provide information about product.

•	If customer enters the product name, the bot provides the recommended product list for the product. Customer can use that product list for while picking the right product of good quality.

•	Customer can also get information about return, refund, amazon prime, etc., using the ChatBot.

•	Customer can click on Get Back button to use other services of Amazon Sentiment Analysis App.

•	Customer can click on Log Out button to log off from the amazon services.

•	Customer can click CTRL+C to stop the server, running in the terminal to provide the service.

•	Once the server is terminated. Customer can click on File->Close Project to close the project.

