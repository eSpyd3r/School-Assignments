# Do not modify this file.

import json
import websocket # must install websocket-client
import threading
import tkinter as tk
from queue import Queue
import traceback

try:
    from image_proc import process_command
except (ModuleNotFoundError, AttributeError):
    print("You must implement the process_command function inside image_proc.py.")

VERSION = 1

def send(data_dict):
    data_dict["VERSION"] = str(VERSION)
    ws = websocket.WebSocket()
    ws.connect("ws://infinite-fortress-70189.herokuapp.com/submit")
    ws.send(str(data_dict).replace("'", '"').encode('utf-8'))
    ws.close()

q = Queue()
def rcv_thread(handle, messages, q):
    def on_open(ws):
        msg = {
            "handle": handle,
            "text": '',
            "version": str(VERSION)
        }
        ws.send(str(msg).replace("'", '"').encode('utf-8'))

    def on_message(ws, message):
        data = json.loads(message)
        if 'challenge' in data:
            messages.insert(tk.END, f"*** SERVER ***: Challenge: {data['challenge']}, <{data['image_string']}>, {int(data['height'])}, {int(data['width'])}")
            try:
                result_image = process_command(data['challenge'], data['image_string'], int(data['height']), int(data['width']))
            except:
                message = f'*** CLIENT ***: Your code produced an exception while running the challenge. The error traceback is as follows:\n{traceback.format_exc()}'
                lines = message.split('\n')
                for line in lines:
                    messages.insert(tk.END, line)
                result_image = ''
            messages.insert(tk.END, f'*** CLIENT ***: You will respond with <{result_image}>.')
            send({'challenge_result': result_image})
        elif 'pass' in data:
            if data['pass'] == 'False':
                messages.insert(tk.END, f"*** SERVER ***: Challenge failed. Disconnecting...")
                q.put('fail')
                ws.close()
            elif data['pass'] == 'True':
                messages.insert(tk.END, f"*** SERVER ***: Challenge passed.")
        else:
            messages.insert(tk.END, f"{data['handle']}: {data['text']}")

    def on_error(ws, error):
        print(traceback.format_exc())
        messages.insert(tk.END, f"*** ERROR ***: {error}")

    def on_close(ws, close_status_code, close_msg):
        messages.insert(tk.END, f"*** SERVER ***: Connection closed by server: {close_msg} ({close_status_code})")
    
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
    window.title('202(#47')

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
    print("Do not run this file directly; instead, run the start_chat module.")