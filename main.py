import openai
import os
import subprocess
import sys

LINUX = 0
WINDOWS = 1
CLIPBOARD_FAILED_MESSAGE = "Current windows is unsupported"

# CONFIG =====================================================================
openai.api_key = sys.argv[1] # Don't worry you can just use a string here
OS = LINUX # LINUX WINDOWS
GPT_MODEL = "gpt-4"
PRE_PROMPT = ""
# ============================================================================

def getClipboardData():
    # Clipboard input
    if OS == LINUX:
        p = subprocess.Popen(['xclip', '-selection', 'clipboard', '-o'], stdout=subprocess.PIPE)
        retcode = p.wait()
        data = p.stdout.read()
        return data.decode('utf-8')  # Decode bytes to string

    elif OS == WINDOWS:
        return CLIPBOARD_FAILED_MESSAGE

    return "Clipboard is not working rn"

def getGPTResponse(prompt_text:str):
    response = openai.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": PRE_PROMPT + prompt_text},
                ]
            )

    return response.choices[0].message.content

def sendNotification(text:str):
    if OS == LINUX:
        # Notification
        subprocess.call(['notify-send', 'Davinci', text])

        # Clipboard output
        p = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
        p.communicate(input=text.encode('utf-8'))

    else:
        print("No clipboard output")

def main():
    data = getClipboardData();
    print(data)
    if data == CLIPBOARD_FAILED_MESSAGE: print("Cliboard failed exiting")

    # GPT prompting
    generated_text = getGPTResponse(str(data))
    print(generated_text)

    sendNotification(generated_text)

main()
