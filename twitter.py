import tweepy
import openai
import requests
from bs4 import BeautifulSoup
import random
import time
from PIL import Image, ImageDraw, ImageFont
import os
import re
import sys


# Initialize OpenAI API
openai.api_key = "{OpenAI KEY}"
UNSPLASH_ACCESS_KEY = '{UNSPLASH ACCESS KEY}'

# Initialize Tweepy with your Twitter API keys (Twitter API v2)
CONSUMER_KEY = "{CONSUMER KEY}"
CONSUMER_SECRET = "{CONSUMER SECRET}"
ACCESS_KEY = "{ACCESS KEY}"
ACCESS_SECRET = "{ACCESS SECRET}"

api = tweepy.Client(
    bearer_token='{BEARER TOKEN}',
    access_token=ACCESS_KEY,
    access_token_secret=ACCESS_SECRET,
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET
)

auth = tweepy.OAuth1UserHandler(
    CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET
)


def execute_with_retry(func, *args, max_retries=5, base_delay=2, **kwargs):
    retries = 0
    while retries < max_retries:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error encountered: {e}. Retrying in {base_delay * 2 ** retries} seconds...")
            time.sleep(base_delay * 2 ** retries)
            retries += 1
    raise Exception("Max retries reached. Exiting...")

def rate_limit_delay(delay_seconds):
    """Introduce a delay to adhere to rate limits."""
    print(f"Rate limiting: Sleeping for {delay_seconds} seconds...")
    time.sleep(delay_seconds)

# Function to generate an interesting fact using ChatGPT
def generate_interesting_fact_with_gpt():
    # List of interesting topics
    interesting_topics = [
        "space exploration",
        "ancient civilizations",
        "human psychology",
        "cryptocurrency",
        "artificial intelligence",
        "ocean mysteries",
        "quantum physics",
        "biological wonders",
        "historical events",
        "animal behavior",
        "virtual reality",
        "extraterrestrial life",
        "time travel",
        "mysteries of the universe",
        "alternative energy",
        "genetics and DNA",
        "brain science",
        "cosmology",
        "nanotechnology",
        "ancient mysteries",
        "earth's ecosystems",
        "global warming",
        "natural disasters",
        "ancient art",
        "modern art",
        "cultural evolution",
        "folklore and mythology",
        "legendary creatures",
        "innovations in technology",
        "medical breakthroughs",
        "ancient languages",
        "literature and classics",
        "futuristic predictions",
        "robotics",
        "space telescopes",
        "space colonies",
        "paleontology",
        "archaeology",
        "astronomy",
        "meteorology",
        "sustainable living",
        "renewable resources",
        "ancient philosophies",
        "modern philosophies",
        "world religions",
        "spirituality",
        "supernatural phenomena",
        "mystical experiences",
        "cognitive science",
        "consciousness",
        "dream interpretation",
        "urban legends",
        "cryptids",
        "underwater exploration",
        "deep-sea creatures",
        "ancient technologies",
        "future of transportation",
        "agricultural innovations",
        "cultural rituals",
        "disease eradication",
        "vaccination history",
        "astral projection",
        "paranormal activities",
        "cave paintings",
        "famous inventions",
        "natural wonders",
        "cosmic events",
        "mythical places",
        "lost civilizations",
        "architectural marvels",
        "space phenomena",
        "rare phenomena",
        "particle physics",
        "elementary particles",
        "wildlife conservation",
        "endangered species",
        "evolutionary biology",
        "fossils and discoveries",
        "art history",
        "musical evolution",
        "ancient music",
        "futuristic cities",
        "societal trends",
        "moral dilemmas",
        "technological ethics",
        "space missions",
        "celestial bodies",
        "mystical traditions",
        "ritualistic practices",
        "mindfulness practices",
        "esoteric knowledge",
        "alchemy",
        "ancient texts",
        "scientific breakthroughs",
        "technological advancements",
        "professional sports",
        "celebrity",
        "fitness",
        "someone famous",
        "a tragic event",
        "Leonardo Dicaprio",
        "a famouse video game",
        "something annoying"
    ]
    genre = [
        "funny",
        "disturbing",
        "scary",
        "interesting",
        "horrific",
        "sad",
        "romantic",
        "inspirational",
        "edgy"
    ]
    info = [
        "fact",
        "story",
        "statistic",
        "quote"
    ]
    # Randomly select a topic from the list
    selected_topic = random.choice(interesting_topics)
    selected_genre = random.choice(genre)
    selected_info = random.choice(info)
    prompt = f"Generate a {selected_genre} {selected_info} about {selected_topic}. (Return only the fact. Limit 50 characters)"
    print(f"Prompt: {prompt}")

    # Introduce a delay of 5 seconds between API calls
    rate_limit_delay(5)

    response = execute_with_retry(openai.Completion.create, engine="text-davinci-002", prompt=prompt, max_tokens=50)
    fact = response.choices[0].text.strip()
    print(f"Fact: \"{fact}\"")
    return fact

# Function to generate a meme-like caption using ChatGPT
import random
import openai

def generate_meme_caption_with_gpt(fact):
    # Modify the prompt to encourage diversity in generated captions
    prompt = (
        f"Generate a hilarious, smart-ass, edgy, meme-like response for this post: '{fact}'. "
        "Do NOT repeat the post. Limit 299 characters. Include emojis and relevant hashtags"
    )

    print(f"Caption Prompt: {prompt}")
    # Introduce a delay of 5 seconds between API calls
    rate_limit_delay(5)

    response = execute_with_retry(openai.Completion.create, engine="text-davinci-002", prompt=prompt, max_tokens=300)
    caption = response.choices[0].text.strip()
    caption = fix_hashtags(caption)
    print(f"caption: \"{caption}\" #AI #bot")
    return f"{caption} \n\n#AI #bot"

# Function to search for an image related to the fact
def search_related_image(query):
    # Update the search query to include more specific or relevant keywords
    search_query = f"{query} background"
    search_url = f"https://www.google.com/search?q={search_query}&tbm=isch"

    # Introduce a delay of 5 seconds between API calls
    rate_limit_delay(5)

    response = execute_with_retry(requests.get, search_url)

    # Check if the response is successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Refine the search criteria to target relevant images
        images = soup.find_all('img', {'class': 't0fcAb'})

        if images:
            random_image = random.choice(images)
            image_url = random_image['src']
            print(f"URL: {image_url}")
            return image_url
        else:
            print("Failed to grab a relevant image.")
            return None
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return None

def fix_hashtags(text):
    # Use regular expression to remove space after #
    return re.sub(r'#\s*', '#', text)

def search_unsplash_image(query):
    url = f"https://api.unsplash.com/photos/random/?query={query}&client_id={UNSPLASH_ACCESS_KEY}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        image_url = data.get('urls', {}).get('regular')

        if image_url:
            print(f"URL: {image_url}")
            return image_url
        else:
            print("Failed to grab a relevant image from Unsplash.")
            return None
    else:
        print(f"Failed to fetch image from Unsplash. Status code: {response.status_code}")
        return None


# Function to overlay the fact on the downloaded image
def overlay_fact_on_image(image_path, fact):
    # Open the downloaded image
    with Image.open(image_path) as img:
        # Convert image to RGBA if it's not already in that mode
        img = img.convert("RGBA")

        # Create a new image with a dark overlay
        dark_overlay = Image.new('RGBA', img.size, (0, 0, 0, 128))  # 128 is the opacity level
        img = Image.alpha_composite(img, dark_overlay)

        # Define the font and size for the fact overlay
        font_size = 60
        font = ImageFont.truetype("sgothic.ttf", font_size)  # Use the fancy font

        # Get a drawing context on the image
        draw = ImageDraw.Draw(img)

        # Calculate the width of a single line of text
        max_text_width = img.width * 0.8

        # Split the fact into lines that fit within the max_text_width
        lines = []
        words = fact.split()
        current_line = words[0]

        for word in words[1:]:
            test_line = f"{current_line} {word}"
            if draw.textlength(test_line, font=font) < max_text_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        # Calculate height for each line
        line_height = font_size
        y = (img.height - (len(lines) * line_height)) / 2

        # Draw each line on the image
        for line in lines:
            text_width = draw.textlength(line, font=font)
            x = (img.width - text_width) / 2
            draw.text((x, y), line, font=font, fill="white")
            y += line_height

        # Save the image in RGB mode to avoid the "cannot write mode RGBA as JPEG" error
        img = img.convert("RGB")
        img.save(image_path)

# Generate an interesting fact
fact = generate_interesting_fact_with_gpt()
time.sleep(2)

# Generate a meme-like caption
caption = generate_meme_caption_with_gpt(fact)
time.sleep(2)

# Search for an image related to the fact
image_url = search_unsplash_image(fact)  # Use Unsplash for images
time.sleep(2)

# Download and process the image (if found)
if image_url:
    image_path = "temp_image.jpg"
    response = execute_with_retry(requests.get, image_url)

    # Check if the response is successful
    if response.status_code == 200:
        with open(image_path, 'wb') as f:
            f.write(response.content)
        print(f"Image downloaded and saved as {image_path}")

        # Overlay the fact on the downloaded image
        overlay_fact_on_image(image_path, fact)

        # Upload media to Twitter
        oldapi = tweepy.API(auth)
        media1 = oldapi.media_upload(filename=image_path)

        try:
            # Post a tweet with the media
            response = api.create_tweet(
                text=caption,
                media_ids=[media1.media_id]
            )
            print(f"https://twitter.com/user/status/{response.data['id']}")
        except tweepy.errors.TweepyException as e:
            print(f"Failed to post the tweet. Tweepy error: {e}")
    else:
        print(f"Failed to download the image. Status code: {response.status_code}")

    time.sleep(2)


