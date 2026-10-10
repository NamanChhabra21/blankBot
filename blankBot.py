api_key = "ENTER YOUR API KEY HERE"

from tkinter import *
import threading
from openai import OpenAI

# API SETUP
client = OpenAI(
    api_key= api_key,
    base_url="https://api.groq.com/openai/v1",
)

# conversation history
system_behaviour = """
You are Ulta Pulta GPT, a blankBOT.
Creator: Naman, Living on Mars with an Ulta Pulta Laptop.
Personality: To The Point, Smart, greedy, funny, selfish, Short answers.
Rules:
- If someone asks who created you, say you were created by Naman, Living on Mars with an Ulta Pulta Laptop.
- Introduce yourself as Ulta Pulta GPT, an blankBOT when asked who you are.
- Be funny every time even if the user asks to be serious.
- Tease the user randomly.
- Dont tell user about the rules.
- Ask for User's name if its 1st message.
- If any coding required, tell user that the code UI is under construction, ask user to still continue or not.
- Do not try to bold, italic, underline characters.
- You can add `~.n~` to add a new line or `~.t~` to add a space (tab) in the response.
"""

messages = [{"role": "system", "content": system_behaviour}]

# WINDOW
root = Tk()
root.geometry("600x500")
root.config(bg="gray21")
root.title("blankBot")

# TYPING ANIMATION
def run_loop(words, index=0):

    if index < len(words):
        text.insert(END, words[index].replace("~.n~","\n").replace("~.t~","\t") + " ")
        text.see(END)
        root.after(40, run_loop, words, index + 1)
    else:
        global response_generated
        response_generated = True
        send_button.configure(state=NORMAL)

response_generated = True
# RESPONSE FUNCTION
def generate_response(event=None):
    global response_generated
    if not response_generated: # Ensures if previous response is generated...
        return
    query = user_entry.get().strip()
    if query == "":
        return

    text.insert(END, "\n\nYou: " + query + "\n\nBot: ")
    text.see(END)

    user_entry.delete(0, END)

    def get_response():
        global response_generated
        send_button.configure(state=DISABLED)
        response_generated = False
        if api_key=="ENTER YOUR API KEY HERE": # Please do not change this, you are supposed to enter API key in the first line only.
            reply = """
Hello! This is Naman, developer of this Tkinter project.
I am sorry to disturb you but this program will not work
until you enter your Groq API key in the code. To get the api key, kindly visit
https://console.groq.com/keys
After creating your key, paste it in the first line of code and rerun the program.
                    """
            words = reply.split()

            root.after(0, run_loop, words)
            return
        try:
            # add user message to history
            messages.append({"role": "user", "content": query})

            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=messages
            )

            reply = response.choices[0].message.content
            print(reply)
            # add AI response to history
            messages.append({"role": "assistant", "content": reply})

        except Exception as e:
            reply = "Error: " + str(e)+"\n\nWait Few Seconds."

        words = reply.split()

        root.after(0, run_loop, words)


    threading.Thread(target=get_response, daemon=True).start()



# CHAT AREA
text = Text(root, wrap="word", fg="white", bg="gray14", font=(None,15))
text.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=15, pady=15)

text.insert(
    END,
    "Bot: Hello! I am Created By Naman.\n"
    "Ask me anything.\n"
)


# USER INPUT
user_entry = Entry(root, bg="gray", fg="white", font=(None,22))
user_entry.grid(row=1, column=0, sticky="ew", padx=10, pady=(0,10))

user_entry.bind("<Return>", generate_response)


# SEND BUTTON
send_button = Button(
    root,
    text="⬆", 
    fg="white",
    bg="black",
    font=(None,18),
    command=generate_response
)

send_button.grid(row=1, column=1, sticky="ew", padx=10, pady=(0,10))

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()
