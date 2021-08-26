# Emojinal

A simple REST API for returning emoji sentiment data based on research from Institut "Jožef Stefan", Slovenia.

## Overview

In planning as series of Miro-based workshops, I've had the idea that participants can express how they feel about different topics/statements/whatever using emojis. While emoji usage is de rigueur in 2021, its meanings aren't strictly codified. Luckily, the Slovenia's Institut "Jožef Stefan" has performed a [massive analysis of emoji usage in tweets, and documented their findings in a research paper](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0144296). As a starting point, I'm calling upon that [data](http://kt.ijs.si/data/Emoji_sentiment_ranking/index.html) to perform some automated analysis of participant sentiment.

## Usage

I'm hosting the API at https://emojin.al/ so [you may contact me if you'd like an API key](mailto:hello@jamesmedd.co.uk). Alternatively you can spin up your own instance using the source code and data provided here.

### Endpoints and authentication

* You can authenticate your request to https://emojin.al/ using the HTTP header `ApiKey`.
* https://emojin.al/sentiment will return emoji sentiment data, with some additional metadata associated with each emoji.
* Non-specific calls made to the above endpoint can be adjusted using query strings for page size and page number: `?page=1&size=5` is the default.
* Specific emojis can be queried like so: https://emojin.al/sentiment/👍
* You can also query emojis using their Unicode codepoint: https://emojin.al/sentiment/128077
* Multiple emojis can be queried simultaneously thus: https://emojin.al/sentiment/👍👎🤌

### Creating a MongoDB collection from the source data

You can use the provided JSON file for your own MongoDB collection. The following command will import the data.

`mongoimport --db emojinal --collection sentiment emojiData.json --jsonArray --maintainInsertionOrder`

I also include separate collection named `keys` to verify users, which you can create manually. A document in that collection looks like:
```
{
    "key": "ASecretKey"
}
```