
# EchoNestPy
A python based API for integrating the Amazon Echo to the Nest Thermostat

EchoNestPy is a python based API server running on flask. It allows the Amazon Echo to talk to the server and then the server will talk to your Nest allowing you to control it. This version is setup to allow multiple Amazon Echo users to share the same server to control their own Nest without interfering with the other users Nests. This means that each Amazon Echo UserID is tied to their own Nest Token and it remembers which Echo UserID is tied to each Nest Token. It uses pickle to write the datastore to a file on the disk so that when the server is restarted it does not require each user to re-authenticate the nest again.

Right now it will control multiple Nests in the same house however when setting the temperature to a set value, it will set all Nests to the same temperature. But when changing the temperature by warmer or cooler it will +/- 2 degrees f to each Nest, even if they are different values. 

Sample Interactions:

* Alexa, Talk to Nest
  * What can I say?
* Alexa, Tell Nest to set the temperature to 76 degrees. 
* Alexa, Tell Nest that I am too warm. 
* Alexa, Tell Nest to turn the temperature up. 

More deatils and videos at: https://zpriddy.com/?p=68

## Requirements and setup

### Local development environment
Your computer or virtual environment needs the following installed before you go any further:

* Python
* [PIP](https://pip.pypa.io/en/stable/installing.html)

To run EchoNestPy, you'll need the python packages specified in [requirements.txt](./requirements.txt).

Once you have the above requirements installed on your computer, clone this repository, and run the following from the project root to get the environment setup for running EchoNestPy:

1. `pip install -r requirements.txt`


### Setting Up Server

The Alexa Skills Kit (ASK) requires that the server has an open connection to the internet on port 443 (HTTPS) with a SSL Certificate (self signed is okay). Right now this runs in flask with out HTTPS but I am looking into changing this. One way to work around this is to use STunnel4 or ngix forwarding to accecpt connections on 443 and connect to the app on port 5000. 

### Setting Up Alexa Skills Kit on Amazon

The ASK is available at: https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/getting-started-guide 

2. Sign in or Create an Account. 
2. Go to Apps & Services at the top of the page
2. Click on Alexa
2. Click Add New Skill
2. Fill out the first form:
** Name: Anything you want it to be - I use Nest Control
** Invocation Name: The hotword to call the app - I have gotten it working with Nest
** Version: 1.0 <- This is hard-coded for now
** Endpoint: https://<domain or ip address>/alexa/EchoPyAPI
2. Go to the next page and copy the intentSchema.json to the Intent Schema and sampleUtterances.txt to the Sample Utterances
2. Go to the next page and upload the selfsigned SSL Cert you have.. and hit next..

### Setting Up Nest Developer Token

Nest developer is available at: https://developer.nest.com

3. Sign In or Create an Account
3. Click on Clients
3. Click Register New Client
3. Fill out the form:
** Name: Anything - I use EchoPy
** Support URL: If you have a domain.. or github?
** OAuth Redirect URL: https://<domain or ip address>/alexa/oauth2
** Make sure that you click on read/write on all options that you can (some are unavailable) and give a short description (you have to..)
3. Click Update Client
3. From the clients page copy the Authorization URL and put it in nestpy_settings.py as nest_auth_uri_1 (sample at SAMPLE_nestpy_settings.py)
3. From the clients page copy the Access Token URL and put it in nestpy_settings.py as nest_auth_uri_3

### Test
At this point you should be able to go to https://<domain or ip address>/alexa/ and see a basic page.. If this works your'e good to go! 


## Usage
````
run: python echopy.py
````

At this time you will have to go to your Echo and say 'Alexa, Talk to Nest' (Replace Nest with what the Invocation Name you set). It should say that you are an unautherized Nest user and to check the card in your Echo App. Open the Echo app and look at the card there. It should give you what your User ID is.. (A bunch of random text) 

Go to https://<domain or ip address>/alexa/auth/<Full UserId> 

This should allow you to authorize it to control your nest. Login to your Nest account and Authorize it.. It should bring you back to the root Alexa page. 

You should be good to start using EchoNestPy


### Notes

The NestPy is another project that I have been working on that I am about to post to github that is a standalone python based API for Nest. 


### To Do:
* Add chnage mode to Nest and Alexa for Away / Home
* Add better support for multi-Nest Households. 
* Add check in time of inbound requests for security.
* Improve sample utterances
* Add better help. 

