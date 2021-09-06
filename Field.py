# Discord stuff
import discord
import asyncio

# Scraping stuff
GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.headless = True

token = "${TOKEN}"
messages = joined = 0

client = discord.Client()

latestTopic = "Adam Trautman has left the field on a cart."
newLatestTopic = ""
upToDate = False
checkInterval = 60


async def scrape_news(timeout):
    while True:
        await asyncio.sleep(timeout)

        # Scraping
        driver = webdriver.Chrome(options=options, executable_path=CHROMEDRIVER_PATH)
        driver.get('https://sleeper.app/topics/170000000000000000')
        results = []
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        driver.quit()

        # Total tag set
        allTags = ["defense", "minor", "hype", "news", "announcement", "breaking"]
        desiredTags = ["defense", "minor", "hype", "news", "breaking"]

        scrapedTopics = []
        # Get each news topic
        for topic in soup.findAll(attrs='topic'):
            # Get metadata for each topic
            tag = topic.find('div', class_="tag").string
            if tag in desiredTags:
                post = topic.find('p').string.replace('“', '').replace('”', '').replace('\n', ' ')
                scrapedTopics.append(post)
                # print('[', tag, ']', post)

        # Write scraped topics to toPost.txt
        writer = open("toPost.txt", "w")
        for t in scrapedTopics:
            writer.write(t + "\n")
        writer.close()

        print("[INFO] Scraping for new posts...")

### Discord

@client.event
async def on_message(message):
    print(message.content)


async def get_news():
    await client.wait_until_ready()

    while not client.is_closed():
        with open("toPost.txt", "r") as f:
            global latestTopic
            global upToDate
            print("Latest Topic: '" + latestTopic + "'")
            for line in f:
                if upToDate is False:
                    global newLatestTopic
                    newLatestTopic = line.replace("\n", '')
                    upToDate = True
                if line.replace("\n", '') != latestTopic:
                    print("[INFO] Writing a new post: '" + line.replace("\n", '') + "'")
                    channel = client.get_channel(${SPECIFIC_CHANNEL_TO_POST_TO})  # news channel
                    await channel.send(line.replace("\n", ''))
                else:
                    print("[INFO] No new posts! Stopping for a bit...")
                    break
            latestTopic = newLatestTopic
            print("[INFO] New Latest Topic: '" + latestTopic + "'")
            upToDate = False
        await asyncio.sleep(checkInterval)

loop = asyncio.get_event_loop()
task = loop.create_task(scrape_news(60))
client.loop.create_task(get_news())
client.run(token)
