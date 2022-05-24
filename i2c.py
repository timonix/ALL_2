command = "SEND_START"
CLK = 10

stage = 0
delay = 0

SDA = 1
SCL = 1
DONE = False

while(not DONE):
    if delay > 0:
        delay = delay - 1

    if command == "SEND_START" and delay == 0:
        if stage == 0:
            SDA = 0
            stage = 1
            delay = CLK/2
        elif stage == 1:
            SCL = 0
            delay = CLK / 2
            stage = 2
        elif stage == 2:
            DONE = True
    if command == "SEND_STOP" and delay == 0:
        if stage == 0:
            SDA = 0
            delay = CLK / 2
            stage = 1
        elif stage == 1:
            SCL = 1
            delay = CLK / 2
            stage = 2
        elif stage == 2:
            SDA = 1
            DONE = True
    print(str(SDA) + "," + str(SCL))