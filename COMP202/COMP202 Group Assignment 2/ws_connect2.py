# Do not modify this file.

import json
import websocket # must install websocket-client
import threading
import tkinter as tk
from queue import Queue
import traceback
import textwrap

try:
    import challenge
except:
    print(f"{traceback.format_exc()}\n\nUnable to import your file challenge.py.")

VERSION = 2

def send(data_dict, ws=None):
    data_dict["VERSION"] = str(VERSION)
    data_s = json.dumps(data_dict)
    
    if ws is None:
        ws = websocket.WebSocket()
        ws.connect("ws://infinite-fortress-70189.herokuapp.com/submit")
    ws.send(data_s)
    if ws is None:
        ws.close()

def insert_message(messages, message):
    lines = message.split('\n')
    
    short_lines = []
    for line in lines:
        if len(line) > 100:
            short_lines.extend(textwrap.fill(line, 100).split('\n'))
        else:
            short_lines.append(line)
    for line in short_lines:
        messages.insert(tk.END, line)
    
    messages.yview(tk.END)

q = Queue()
def rcv_thread(handle, messages, q):
    def on_open(ws):
        msg = {
            "handle": handle,
            "version": str(VERSION)
        }
        send(msg, ws)

    def on_message(ws, message):
        data = json.loads(message)
        print(data)
        if 'challenge_arguments' in data:
            if 'text' in data:
                insert_message(messages, "*** CLIENT ***: " + data['text'])
            
            args = ', '.join([f'{param}={arg}' if type(arg) != str else f"{param}='{arg}'" for param, arg in data['challenge_arguments'].items()])
            insert_message(messages, f"*** SERVER ***: Challenging function {data['challenge_function']} with arguments {args}")
            try:
                func = getattr(challenge, data['challenge_function'])
            except:
                insert_message(messages, f"{traceback.format_exc()}\n*** CLIENT ***: Function {data['challenge_function']} could not be found in challenge.py.")
                return
            
            try:
                assert type(data['challenge_arguments']) is dict
                result = func(**data['challenge_arguments'])
            except:            
                message = f'*** CLIENT ***: Your code produced an exception while running the challenge. The error traceback is as follows:\n{traceback.format_exc()}'
                lines = message.split('\n')
                for line in lines:
                    insert_message(messages, line)
                result_image = ''
                return
            
            insert_message(messages, f'*** CLIENT ***: You will respond with <{result}>.')
            send({'challenge_result': result, 'handle': handle, 'challenge_function': data['challenge_function']})
        elif 'pass' in data:
            if data['pass'] == 'False':
                insert_message(messages, f"*** SERVER ***: Challenge failed.")
            elif data['pass'] == 'True':
                insert_message(messages, f"*** SERVER ***: Challenge passed.")
            insert_message(messages, data['text'])

        elif 'description' in data:
            insert_message(messages, data['room_name'])
            insert_message(messages, data['description'])
        elif 'room_name' in data:
            insert_message(messages, f"[{data['room_name']}] {data['handle']}: {data['text']}")
        else:
            insert_message(messages, f"{data['handle']}: {data['text']}")
    
    def on_error(ws, error):
        print(traceback.format_exc())
        insert_message(messages, f"*** ERROR ***: {error}")

    def on_close(ws, close_status_code, close_msg):
        insert_message(messages, f"*** SERVER ***: Connection closed by server: {close_msg} ({close_status_code})")
    
    ws_rcv = websocket.WebSocketApp("ws://infinite-fortress-70189.herokuapp.com/receive",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    ws_rcv.run_forever(ping_interval=3)

def send_from_input_field(messages, handle, text_input):    
    text = text_input.get()
    text_input.delete(0, tk.END)
    if not q.empty():
        messages.insert(tk.END, f"*** CLIENT ***: You were disconnected and cannot send further messages.")
        return
    send({
        'handle': handle,
        'text': text
    })

def start_gui(handle):
    if handle == 'your name here':
        raise ValueError("You must edit the HANDLE variable to your username.")
    window = tk.Tk()
    window.title('infinite-fortress-70189')

    frm_messages = tk.Frame(master=window)
    scrollbar = tk.Scrollbar(master=frm_messages)
    messages = tk.Listbox(
        master=frm_messages, 
        yscrollcommand=scrollbar.set
    )
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
    messages.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    frm_messages.grid(row=0, column=0, columnspan=2, sticky="nsew")

    frm_entry = tk.Frame(master=window)
    text_input = tk.Entry(master=frm_entry)
    text_input.pack(fill=tk.BOTH, expand=True)
    text_input.bind("<Return>", lambda x: send_from_input_field(messages, handle, text_input))
    text_input.insert(0, "Your message here.")

    btn_send = tk.Button(
        master=window,
        text='Send',
        command=lambda: send_from_input_field(messages, handle, text_input)
    )

    frm_entry.grid(row=1, column=0, padx=10, sticky="ew")
    btn_send.grid(row=1, column=1, pady=10, sticky="ew")

    window.rowconfigure(0, minsize=500, weight=1)
    window.rowconfigure(1, minsize=50, weight=0)
    window.columnconfigure(0, minsize=500, weight=1)
    window.columnconfigure(1, minsize=200, weight=0)

    window.update_idletasks()
    window.update()
    
    rcv_t = threading.Thread(target=rcv_thread, args=(handle, messages, q))
    rcv_t.start()
    
    window.mainloop()

if __name__ == '__main__':
    print("Do not run this file directly; instead, run the chat2.py module.")