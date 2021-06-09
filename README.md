# A Journey Through the TCP/IP Model

Written by [Alex Wyatt](https://github.com/227345554) and [Angel Thanur] (https://github.com/21967284).

##Project Brief

This app was developed as a part of CITS3403 (Agile Web Development). The task was to write a web application that simulates a learning experience on any topic, applies some assessment and feedback of these learning at the end. 

The app was written using HTML, CSS, JavaScript (AJAX, Jquery, bootstrap) and Python(Flask).

##Application Overview
**A journey through the TCP/IP Model** is an educational app designed to help IT students understand the TCP/IP model of networking. It aims to simplify networking concepts by using plain and fun language to describe complex topics and uses 'bite-sized' information to avoid intimidating students. 

For each of the layers in the TCP/IP Model (Link, Network, Transport, Application), there are short explanations describing the key information about each layer. After each explanation section, there is a quiz section, where users can test their understanding. Users can submit their quiz answers and receive results on their progress. 

A user must login to be able to access the explanation and quiz content. Once a user is logged in, they are provided access to the very first layer (ie the Link Layer). Once they've read through this module and completed the quiz, then they will be able to proceed to the next layer (ie the Network Layer). Students must complete the previous layer module before accessing the next one. 

At any given stage, users can also view their overall progress and accuracy stats by clicking on the **Progress** link

There is also an additional **admin** functionality. To avoid students registering themselves as admins, the link to register as admin is currently hidden. 

Admins may create additional questions via the **Manage Questions** link. The quiz forms for each layer is dynamically generated so that admins may add however many questions they deem necessary to test a student's understanding.

This app has also been created with mobile-responsiveness in mind. The best place to see mobile responsive behaviour is in: 
* nav-bar - the nav-bar will contract down to just icons and space themselves out in mobile/small device mode
* progress page - this page's tile will automatically re-arrange themselves to scroll horizontally when in mobile/small device mode
* All other pages - The content on all other pages (e.g. content, explanation, quiz, results, login, register) will also shrink/expand according to device size


##Libraries used
* [Chart.js](https://www.chartjs.org/)
* [Boostrap](https://getbootstrap.com/)
* [jQuery](https://jquery.com/)


##To test this project functionality
Install python and pip
```
pip3 install -r requirements.txt
export FLASK_APP=networking.py
flask db migrate
flask db upgrade
flask run
```
To set up the data required to test and demonstrate functionality, go to: 
 [localhost:5000/autopopulate](https://localhost:5000/autopopulate)
 
This script will pre-load questions in the database and create 2 logins: 

Standard user account: 

    username: test
    password: test

Admin user account:

    username: admin
    password: admin
    
To reset the state of database, use: [localhost:5000/autoclear](https://localhost:5000/autopopulate)
