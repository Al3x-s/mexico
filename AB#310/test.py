import sys, time, keyboard, threading
def ps(description, delay=0.02):
    def input_listener():
        nonlocal skip_print
        while True:
            keyboard.wait('s')
            skip_print.set()
    

    skip_print = threading.Event()
    input_thread = threading.Thread(target=input_listener)
    input_thread.daemon = True
    input_thread.start()


    for char in description:
        if skip_print.is_set():
            break
        print(char, end='', flush=True)
        time.sleep(delay)


ps("---------------------------------------------------------------------------")
print("dumbass")
