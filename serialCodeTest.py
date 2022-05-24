done = 0
started = False
message = [1, 0, 1, 0, 1, 0, 1, 0]
message.reverse()
timer = 0
i = 0
output = 1

for loop in range(100):
    if timer > 0:
        timer = timer - 1

    if loop == 20:
        started = True

    if started:
        started = False
        timer = 5
        output = 0
        done = 1
        i = 0

    if timer == 0:
        if done == 0:
            output = 1
        else:
            # print(message)
            output = message[-1]
            message.pop()
            done = i ^ 7
            i = i + 1
            timer = 5
    print(output, end=",")
