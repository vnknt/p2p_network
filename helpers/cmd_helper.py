def mergeCmd(cmd,msg):

    message=f"{cmd}({msg})"
    print(message)
    return message







def splitCmd(cmd,msg):
    length=len(cmd)

    message=msg[length+1:-1]
    print(message)
    return message

    