import codecs
import string
import json

import pathlib
import unittest

import nltk
from nltk.corpus import cess_esp

from ia.txt import NLP
from bd.entidades import Kiosco
import tweepy

class TestTweepy(unittest.TestCase):

    def test_trends_place(self):
        claves = open("twitter.keys", "r")
        json_claves = json.load(claves)
        consumer_key = json_claves['consumer_key']
        consumer_secret = json_claves['consumer_secret']
        access_token = json_claves['access_token']
        access_token_secret = json_claves['access_token_secret']
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        tendencias = api.trends_place(468739)
        return 1


if __name__ == '__main__':
    unittest.main()