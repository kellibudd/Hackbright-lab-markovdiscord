"""Generate Markov text from text files."""

import discord
import os
from random import choice


def open_and_read_file(input_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    contents = open(input_path).read()

    text_string = contents.split()

    return text_string

def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']
        
        >>> chains[('there','juanita')]
        [None]
    """
  
    chains = {}

    # loops through string of text until there are only 2 strings left
    # creates keys in chains dict which are made up of two-word pairs
    # creates new value for every word that follows the key (two-word pair)

    for i in range(len(text_string)-2):

        key = text_string[i], text_string[i + 1]
        value = [text_string[i + 2]]

        chains[key] = chains.get(key, []) + value

    return chains


def make_text(chains):
    """Return text from chains."""

    key = choice(list(chains.keys()))
    words = [key[0], key[1]]

    # while True:
    #     if key[0][0].isupper()== True:
    #         words = [key[0], key[1]]

    while key in chains:

        value = choice(chains[key])
        key = (key[1], value)
        words.append(value)

    return " ".join(words)

    # your code goes here


input_path = "green-eggs.txt"

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text)

# Produce random text
random_text = make_text(chains)

client = discord.Client()

@client.event
async def on_ready():
    print(f'Successfully connected! Logged in as {client.user}.')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('get message'):
        await message.channel.send(make_text(chains))

    if message.content.startswith('say hi to my friend'):
        await message.channel.send("Hi Laura! You're the smartest... don't ever change!")

client.run(os.environ['DISCORD_TOKEN'])
