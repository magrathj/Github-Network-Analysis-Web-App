
from uuid import uuid4
from flask import Flask,  abort, request
import requests
import requests.auth
import urllib.parse
from flask import redirect
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['github_db']


coll_users = db['users'] # this should hold the user logging into the site
coll_repos = db['repos'] # this should be all users
coll_followers = db['followers'] # this should be all of the users who are followers of the login user
coll_followering = db['followering'] # this should be all of the users who are followering of the login user


def get_all_users():
    login = []
    for x in coll_users.find().sort("login", -1):
        login.append(x['login'])
    return(login)


def get_specific_user(login_name):
    myquery = { "login": login_name }
    mydoc = coll_users.find(myquery)
    for x in mydoc:
        print(x)


def get_users_repos(login_name):   
    myquery = { "full_name": { "$gt": login_name } }
    mydoc = coll_repos.find(myquery)
    for x in mydoc:
        print(x)


def drop_collections():
    coll_users.drop()
    coll_repos.drop()
    coll_followers.drop()
    coll_followering.drop()


def main():
    names = get_all_users()
    for x in names:
        print(x)


if __name__ == '__main__':
    main()
	