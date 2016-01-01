#SUMA

Suma stands for **S**hort **U**RL **M**anagment **A**pp.
The role of Suma to manage external links and extract data from them, Suma is a small web service to easily do the following:

- Creating short URL for external link within your application
- Extracting Title
- Capturing Screenshot from URL 
- Blocking URL's
- Collecting clicks

If your application needs to display external links then it's probably important that you don't redirect the user directly to the URL so you fight spam, phishing attacks or inappropriate links.

Suma is at an early stage of development, but the goal of this project is to provide a microservice which covers the basic need for a company to protect their users from external links within their products. You can read more about the motivation behind Suma [here](http://rachbelaid.com/introducing-suma)

##Use cases

If you don't understand directly what Suma is for. Let's illustrate it with few use cases:

- Public Feeds (eg: Twitter or FB like app) which allow user to post link publicly
- Reviews or comments allowing external links
- Display link title or screenshot to preview an external link within your application (eg: slack like app)

To summarize: if your application allows external links from users, then Suma can be useful.

##Project Structure and Usage

Suma is composed of 2 web applications. A private API to manage the links and a public API to handle the link redirection and statistic collection.

Suma is structured this way to make it easier to protect the private API. The private API shouldn't be exposed to the outside world and it has to be used via your application as a microservice.

Eg. User Jane Doe shares a comment which contains a link. Your application detects a link, then calls Suma to convert this link, then your application handles the substitution.

For now, it is the responsibility of your application to handle detection and substitution of links. Maybe in the future, we could add some helpers.

The code of the private API is located in `suma/api` and the code of the public API is located `suma/web`.

##Installation

###Requirements

- Python 2.7
- Postgres 9.3+
- Redis
- Phantomjs (for the screenshots)
- Unix Base operating system

### Creating an environment

The first thing you’ll need is the Python virtualenv package. You probably already have this, but if not, you can install it with:

    pip install virtualenv

Once that’s done, choose a location for the environment, and create it with the virtualenv command. 

    virtualenv ~/.virtualenv/suma/

Finally, activate your virtualenv:

    source ~/.virtualenv/suma/bin/activate

Now that you have an environment setup, you can proceed to the installation of Suma

### Installing Suma 

You can install Suma and all its dependencies with the `pip` command used to install virtualenv:

    pip install suma

If you plan to use s3 then you install the Suma with the s3 dependencies.

    pip install suma[s3]


###Configuration files

To run Suma, you will need to create 2 ini files which follow the [Paste.Deploy](http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/paste.html) format.
We provide 2 examples of files to run suma:

- [api.ini](https://github.com/rach/suma/blob/master/examples/api.ini) to run the private API.
- [web.ini](https://github.com/rach/suma/blob/master/examples/web.ini) to run the public API.

Within these files you need to change at least these 2 important settings:

- `sqlalchemy.url` to a dsn representing your database settings. For more info, you can read more about it [here](http://docs.sqlalchemy.org/en/latest/core/engines.html). Suma only supports PostgreSQL so you cannot use a dsn for another RDBMS

- `hashid.secret` to a secret of your choice. The secret is used to generate different short URL's per installation

You can also configure these others settings if you aren't happy with the values in the files' examples:

- `celery.broker_url` is dsn of a broker URL. We suggest that you use redis but celery supports other brokers. You can refer to the celery [documentation](http://docs.celeryproject.org/en/latest/getting-started/brokers/) for more info.

- `storage.s3` is a boolean to choose between s3 or local storage for the screenshots. This setting is set to `false` by default for using the local filesystem.

- `storage.local.base_path` a local path to where to create the screenshots if you are using local storage 
- `storage.local.base_url`: this is the URL where the application accesses the screenshots if you are using local storage. By default, the public api can serve the screenshots if you set the value to a relative URL (eg: `/storage`).

- `storage.s3.base_url`: the url where the screenshot can be accessed from if you are using s3.
- `storage.s3.bucket_name`: the name of the s3 bucket
- `storage.s3.access_key`: the access key id to write in the s3 bucket
- `storage.s3.secret_key`: the secret key id to write in the bucket
- `suma.tasks`: a list of tasks to run on the URL. The possible tasks are `html`, `text`, `screenshot` and `title`.

### Database

Suma uses PostgreSQL. It is not required to create a new database if you are using PostgreSQL already because Suma uses a different schema than public to avoid conflicts.

After installing and configuring Suma, you can create the required tables and schema with:

    # activating the virtualenv
    source ~/.virtualenv/suma/bin/activate


    initialize_suma_db application.ini


###Running Suma

We provide 2 examples of config files with already a section to run `uWSGI` with some basic settings. First, you need to install [uWSGI](https://pypi.python.org/pypi/uWSGI). 

    # activating the virtualenv
    source ~/.virtualenv/suma/bin/activate


    # installing dependencies to run suma 
    pip install uwsgi


    # running the private api on the port 8081
    uwsgi --ini examples/api.ini  


    # running the private api on the port 8081
    uwsgi --ini examples/web.ini 


    # running the background workers to collect link data 
    celery worker -A suma.celery --ini examples/api.ini
    
We suggest that you use uWSGI because it has a good support for [PasteDeploy](https://pypi.python.org/pypi/PasteDeploy). You need to configure the uWSGI's settings to run the application as you prefer (eg: socket + nginx)

##Background Tasks

Suma can run 4 types of background tasks:

- `html` to store the HTML from the URL. This can be used as page cache or to run operations on it.
- `text` to extract the main content from the URL. This can be used to display the content preview.
- `screenshot` to generate a screenshot from the URL. This can be used to display thumbnails preview within your application.
- `title` to extract the title from the URL. This can also be used for preview.

##Banning Rules

When you ban a URL you can have 3 modes:

- `url`: to ban exactly identical URL's
- `netloc`: to ban any URL which matches the same FQDN
- `path`: to ban any URL which matches FQDN and the path without considering the query string or an anchor.

To illustrate the rules let's assume these 3 urls:

- https://google.com/test
- http://google.com/test?something=1#title
- https://google.com/random

if we ban `https://google.com/test` with mode `url` then only `https://google.com/test` will be blocked.

if we ban `https://google.com/test` with mode `path` then  `https://google.com/test` and `http://google.com/test?something=1#title` will be blocked.

if we ban `https://google.com/test` with mode `path` then all the URL's above will be blocked.

##API's

###Private

The private API allows you to create, ban links and refresh link's data.

####Create link

Create a link in Suma for a specific URL. You can also use a `user_id` to generate different links for the same url. 

    POST /links

#####Parameters


| Name      | Type      | Required | Description                                                 |
| --------- |:---------:|:--------:| ----------------------------------------------------------- |
| url       | string    | true     | The url that you want to create a link for                  |
| user_id   | integer   | false    | To have different links created for same URL between users  |


#####Payload

    {
      "url": "https://google.com",
    }

or using `user_id`:

    {
      "url": "https://google.com",
      "user_id": 42,
    }
    
#####Response

Status: 201 Created

Content-Type: application/json

    {
      "data": {
        "attributes": {
          "title": null,
          "screenshot": null,
          "updated": "2015-12-18T08:20:27.929472",
          "created": "2015-12-18T08:20:27.929472",
          "url": "https://google.com",
          "banned": false,
          "hashid": "KEYaED",
          "clicks": 0
        },
        "type": "links",
        "id": 1
        "actions": {
          "ban": {
            "links": {
              "related": "http://private-api/links/2/ban"
            }
          },
          "text": {
            "links": {
              "related": "http://private-api/api/links/2/text"
            }
          },
          "html": {
            "links": {
              "related": "http://private-api/api/links/2/html"
            }
          },
          "refresh": {
            "links": {
              "related": "http://private-api/api/links/2/refresh"
            }
          }
        }
      }
    }

This API return a `201` status if a new link has been created, otherwise it returns a `200` status if a link already exists for the received `url` and `user_id`. When you create a new Link, the `title` and the `screenshot` attributes will be `null` because they are generated asynchronously via the background workers. 

###Get link

Return the existing link for these `id` or `hashid`.

    GET /links/:id
    GET /links/:hashid
    
####Response

Status: 200

Content-Type: application/json

    {
      "data": {
        "attributes": {
          "title": "Google",
          "screenshot": "http://url-to-screenshot",
          "updated": "2015-12-18T08:20:27.929472",
          "created": "2015-12-18T08:20:27.929472",
          "url": "https://google.com",
          "banned": false,
          "hashid": "KEYaED",
          "clicks": 0
        },
        "type": "links",
        "id": 1
        "actions": {
          "ban": {
            "links": {
              "related": "http://private-api/links/2/ban"
            }
          },
          "text": {
            "links": {
              "related": "http://private-api/api/links/2/text"
            }
          },
          "html": {
            "links": {
              "related": "http://private-api/api/links/2/html"
            }
          },
          "refresh": {
            "links": {
              "related": "http://private-api/api/links/2/refresh"
            }
          }
        }
      }
    }

This endpoint returns 404 if there is no link matching the `id` or `hashid`.

###Ban Existing Link

    POST /links/:id/ban
    POST /links/:hashid/ban

####Parameters


| Name      | Type      | Required | Description                                                      |
| --------- |:---------:|:--------:| ---------------------------------------------------------------- |
| mode      | string    | false    | one of these values: "url", "path" or "netloc". Default to "url"" |


#####Payload

    {
    }

or with `mode`:

    {
      "mode": "netloc",
    }



###Ban a URL

You can ban a URL even if no link exists yet in the database. It will automatically ban any future links created which match the criteria. 

    POST /ban

####Parameters


| Name      | Type      | Required | Description                                                 |
| --------- |:---------:|:--------:| ----------------------------------------------------------- |
| url       | string    | true     | The url that you want to ban                                |
| mode      | string    | false    | one of these values: "url", "path", "netloc"                 |


####Response

Status: 201

Content-Type: application/json

###Get Link's HTML

If you enable the `html` task then Suma stores the HTML of a URL so you can retrieve it later.

    GET /links/:id/html
    GET /links/:hashid/html

####Response

Status: 200

Content-Type: text/html

If the value doesn't exist then you will receive a 204 (No Content) 

###Get Link's text

If you enable the `text` task then Suma tries to get the main content of a URL using [Goose](https://pypi.python.org/pypi/goose-extractor/). This can be useful for articles to display the content for preview. 

    GET /links/:id/text
    GET /links/:hashid/text

####Response

Status: 200

Content-Type: text/plain

If the value doesn't exist then you will receive a 204 (No Content) 

##Public API

###Access Link (Redirect)

    GET /:hashid 

Accessing the hashid of the public API will return a Permanent Redirect (301) to the URL and increment the clicks counter.

###Access Link Screenshot (Redirect)

    GET /:hashid/screenshot 

Accessing this endpoint will return a Temporary Redirect (302) to the screenshot URL

##Questions

If you've met any difficulties or have questions, you can ask them via [gitter](gitter.im/rach/suma)

##Contribute

The project is young so there are quite a few things that you can do if you want to contribute:

- Testing the application and report bugs
- Improving the documentation to cover more installation instructions
- Add a Dockerfile, Compose file
- Improving the API's
- Improving coverage
- Reviewing indexes
- Correcting my English (Sorry, I'm not a native English speaker)
 
Any help is appreciated.

##License

Suma is licensed under Apache V2 license, the full license text can be found [here](https://github.com/rach/suma/blob/master/LICENSE)
