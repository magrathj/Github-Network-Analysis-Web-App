
from uuid import uuid4
from flask import Flask,  abort, request
import requests
import requests.auth
import urllib.parse
from flask import redirect
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['github_db']


coll = db['users']
coll_repos = db['repos']
coll_followers = db['followers']
coll_followering = db['followering']


def get_user(login_name):
    for x in coll.find().sort("login", -1):
        print(x)
        #get_user_details(login_name)

def get_user_details(login_name):   
    myquery = { "full_name": { "$gt": login_name } }

    mydoc = coll_repos.find(myquery)

    for x in mydoc:
        print(x)

def main():
    get_user_details(login_name="daattali")


if __name__ == '__main__':
    main()
	