# MuseScore-Statistics

As an active MuseScore user, I have found that the statistics page misses some important statistics, such as total views and favourites, or average statistics.

To fix that, I wrote a small script in Python to scrape the statistics and calculate them accordingly. There are two scripts provided:

These scripts require the Python Selenium library:
```pip install selenium```

### General.py

This script loops through all of a user's sheet music pages and scrapes the statistics for each score one by one. It is slow and does not include private or unlisted scores, but it allows anyone to scrape anyone's statistics.

#### Usage: 
```python3 General.py```
### Pro.py

For pro users, the statistics feature conveniently lists all of the statistics for each score. This script scrapes the statistics for each score and calculates the total and average statistics. It is much faster than `general.py`, and it includes private and unlisted scores. However, it is only available to MuseScore users with a PRO account, and requires a manual login (the script can't pass the ReCaptcha).

#### Usage: 
```python3 Pro.py```
Follow the instructions accordingly.

