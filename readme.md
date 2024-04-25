# Check for Chapter Updates

---

This small script will check for chapter updates from your desired novel from the website [webnovelworld](https://www.webnovelworld.org/). Upon finding a new chapter, it will send an SMS message to your phone with the chapter name and number. This script is desgined specifically for this website, but will work with any novel on this website (as far as I have tested).

## How it Works

First we scrape the base novel/chapters url from the site, locating the specific element that is used to go to the final page in the pagination container. After scraping this new portion of the site, we find the list of chapters and compare the most recent 8 chapters with what we have in our latest_chapter. If it is not the same, then it is a new chapter for us and it will send an SMS message.
This script will run every 10 minutes.

## How to set it up

If you are looking to use this, the configTemplate contains the directions for what to fill it out with. Upon setting up the config file, rename it to config.ini and then run the script. Be sure to udpate the latest_chapter with the current latest chapter of the novel, or a few chapters behind to test the script with your mobile number.

I have provided a list of Canadian Gateways for those in my home country. I am unsure of the ones for any other providers outside of Canada.

## Why?

This was something I made for myself to let me know when chapters of novels I was reading have been released, since there is no set schedule for these releases and it can sometimes be days apart. Instead of spending time checking multiple times a day, I can simply leave this script runnning on my raspberry pi or any alternate device.

Copyright @2024 jmuell
