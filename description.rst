SUMA
####

Suma stands for **S**\ hort **U**\ RL **M**\ anagment **A**\ pp.
The role of Suma to manage external links and extract data from them, Suma is a small web service to easily do the following:

- Creating short URL for external link within your application
- Extracting Title
- Capturing Screenshot from URL 
- Blocking URL's
- Collecting clicks


Use cases
---------

If you don't understand directly what Suma is for. Let's illustrate it with few use cases:

- Public Feeds (eg: Twitter or FB like app) which allow user to post link publicly
- Reviews or comments allowing external links
- Display link title or screenshot to preview an external link within your application (eg: slack like app)

To summarize: if your application allows external links from users, then Suma can be useful.

Project Structure and Usage
---------------------------

Suma is composed of 2 web applications. A private API to manage the links and a public API to handle the link redirection and statistic collection.

Suma is structured this way to make it easier to protect the private API. The private API shouldn't be exposed to the outside world and it has to be used via your application as a microservice.

Installation
------------

The installation instructions can be found in the `README <https://github.com/rach/suma>`_ of the project.

License
-------

Suma is licensed under Apache V2 license, the full license text can be found `here <https://github.com/rach/suma/blob/master/LICENSE>`_
