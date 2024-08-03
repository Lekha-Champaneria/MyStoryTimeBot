import telebot
import requests
import re
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
GEMINI_API_KEY = "GEMINI_API_KEY"
TOKEN: Final = 'YOUR_TELEGRAM_BOT_TOKEN'  # Replace with your Telegram bot token
BOT_USERNAME: Final = '@BOT_USERNAME'  # Replace with your bot username
bot = telebot.TeleBot(TOKEN)


def show_options():
    try:
        choice = int(input("""Select your favourite genre of story:
        1: Horror
        2: Comedy
        3: Adventure
        4: Mystery
        5: Fantasy
        6: Cancel
        """))
        # return choice
        genre_options = {
            1: "Horror",
            2: "Comedy",
            3: "Adventure",
            4: "Mystery",
            5: "Fantasy"
        }
        # Handle genre selection
        if choice in range(1,6):
            genre = genre_options[choice]
            print(genre)
            print(type(genre))
            initiate_story(genre)
        elif choice == 6:
            print("Ok, May be next time! 👋")
            exit(1)
        else:
            print(f"Please select an option from 1 to {len(genre_options)+1}\n")
            print(type(choice))
            show_options()
        return choice
            # generate_story(choice, {})
    except ValueError:
        print("Please select a valid Genre\n")
        show_options()

def initiate_story(genre:str):


    # Craft the Gemini prompt based on user input
    prompt = f''' /
        **Objective:** Generate engaging story paragraphs with user choice options.

        **Context:**

        Genre: {genre}

        **Storytelling Loop:**

        1. **Initial Prompt:**
            * the story must be relatable to the user, make sure to give a POV like starting with "You" so that they feel being part of the story instead of being third person
            * Craft an opening paragraph considering the genre/concept.
            * Include two clear and concise choice options for the user.

        **Important Notes:**
            * Go DEEP inside the genre while creating the story
            * MAKE SURE to use simple indian english words so that every user can understand easily
            * Focus on paragraphs and options.
            * Maintain story cohesion.
            * Adapt to genre.
            * Always give response containing exactly three things  (1. "Phrase", 2. "Option 1", 3. "Option 2")
            * Paragraph must be started exactly with "**Text**"
            * Options must be started exactly with "**Option 1**" and "**Option 2**" REMEMBER, EXACTLY THIS
    '''
    return parse_generated_text(send_request(prompt,genre))

def send_request(prompt:str,genre:str):
    # Prepare the API request data containing the prompt
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                ],
            },
        ],
    }

  # Send the request to Gemini API
    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}",
        json=data
    )
    try:
        if response.status_code == 200:
            generated_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            return generated_text
        else:
            return None
    except KeyError:
        print("Error aai tu nikal love day")

def select_option(choice):
    try:
        choice = int(choice)
        if choice == 3:
            print("Great choice! Ending the story with the climax...")
            return choice
        elif choice in range(1, 3):
            return choice
        else:
            print("Enter a valid choice between 1 to 3")
            select_option(choice)
    except ValueError:
        print("Enter a valid choice between 1 to 3 number only")
        select_option(choice)

def continue_story(history:dict,genre:str):
    if len(history) <= 3:
        history_for_prompt = ""
        for i,pair in history.items():
            history_for_prompt += f"paragraph {i}: {pair[0]}\n user_choice{i}: {pair[1]}"
        continue_prompt = f'''
            I have a list of story phrases and user selected options, that means the story is interactive.
            The list is given below {history_for_prompt}, the genre is {genre}.
            Now, your task is to continue the story by generating next paragraph with exactly 2 options.
            There are some points to keep in mind listed below:

            **Story Continuation:**
            * Based on the user's chosen option and the Gemini API response (paragraph):
                * Generate a new paragraph with options, reflecting the user's choice and the API response.
                * Maintain logical narrative flow.

            **Important Notes:**
            * Go DEEP inside the genre while creating the story
            * MAKE SURE to use simple indian english words so that every user can understand easily
            * Focus on paragraphs and options.
            * Maintain story cohesion.
            * Adapt to genre.
            * Always give response containing exactly three things  (1. "Phrase", 2. "Option 1", 3. "Option 2")
            * Paragraph must be started exactly with "**Text**"
            * Options must be started exactly with "**Option 1**" and "**Option 2**" REMEMBER, EXACTLY THIS
        '''
        return parse_generated_text(send_request(continue_prompt,genre))
    # else:
    #     terminate_stroy(history=history, genre=genre)


def terminate_stroy(history:dict,genre:str):
    Ending_Prompt = f'This is the list of story phrases and choices by a user for {genre} genre: '
    for i, pair in history.items():
        Ending_Prompt += f"Phrase {i}: "
        Ending_Prompt += str(pair[0])
        Ending_Prompt += f", User choice{i}: {str(pair[1])}\n"
    Ending_Prompt += '''
        Your task is to Conclude the story and return a paragraph of conclusion.
        keep in mind the genre and the user choices based on situations, And make sure to end the story in a very logical and preferable to user
        You don't need to give any explainations or any other response, ONLY GIVE THE PLAIN TEXT OF CONCLUSION PARAGRAPH

        **Important Notes:**
            * Go DEEP inside the genre while creating the story
            * MAKE SURE to use simple indian english words so that every user can understand easily
            * Focus on paragraphs and options.
            * Maintain story cohesion.
            * Adapt to genre.
            * Paragraph must be started exactly with "**Text**"
    '''
    response = send_request(Ending_Prompt,genre)
    pattern = r"\*\*(.*?)\*\*"  # Matches text between any number of asterisks (*)
    return re.sub(pattern, "", response)

def parse_generated_text(text):
    try:
        # Split the text by line breaks
        lines = text.splitlines()
        line_copy = lines.copy()
        # print("length : ",type(lines))

        GeneratedParagraph = [] #Bharat Sarkar
        for line in lines:  #Yojna na 10 Crores
            if line.startswith("**Option 1**") or line.startswith("**Option 1:**") or line.startswith("**Option 2**") or line.startswith("**Option 2:**"):
                break
            GeneratedParagraph.append(line)
            line_copy.remove(line)
        lines = line_copy.copy() #Sarkar khai gaya 5 Crores bachya

        option1 = []  #Gujarat Sarkar
        for line in lines:
            if line.startswith("**Option 2**") or line.startswith("**Option 2:**"):
                break
            option1.append(line)
            line_copy.remove(line)
        lines = line_copy #Sarkar kkhai gayi 3 Crores bachya 2 crores

        option2 = lines #Bachha-kuchha jnata ne apya

        pattern = r"\*\*(.*?)\*\*"  # Matches text between any number of asterisks (*)
        for i in range(len(GeneratedParagraph)):
            GeneratedParagraph[i] = re.sub(pattern, "", GeneratedParagraph[i])
        for i in range(len(option1)):
            option1[i] = re.sub(pattern, "", option1[i])
        for i in range(len(option2)):
            option2[i] = re.sub(pattern, "", option2[i])

        x=''
        for i in GeneratedParagraph:
            x+=i
        y=''
        for i in option1:
            y+=i
        z=''
        for i in option2:
            z+=i

        return [x, y, z]
    except AttributeError:
        return ['try again later',"Don't Press","these buttons"]
