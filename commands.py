#  Declare constants to send to client in response to commands

password_list = "Passwords:\n\r1 = Q9mtw-%H\n\r2 = 9QuXU!dY\n\r3 = 64vXm(a@\n\r4 = >x3EM)(-\n\r5 = m3/^-HK9\n\r" \
                "6 = qLk[]4Ya\n\r7 = MN/&Zf!9\n\r8 = yC[Ep5eq\n\r9 = 9=p/t!DC\n\r10 = _4PYLwVZ\n\r11 = .j6QB5bK\n\r" \
                "12 = vjL3_NSE\n\r13 = 6T=c^Rh]\n\r14 = =7nQ69>D\n\r15 = ByMk5u)s\n\r16 = 3&Q$bE!x\n\r" \
                "17 = [-9b!YLv\n\r18 = RGt*_b-7\n\r19 = /D4{(VAt\n\r20 = RmdEyZ9/\n\r21 = v}V)9bjw\n\r" \
                "22 = VFm5D/Qq\n\r23 = 5RE@MJ)t\n\r24 = %6$/Pz5E\n\r25 = 72uPe_CR\n\r26 = j8sQ_ChR\n\r" \
                "27 = j(N8qfa7\n\r28 = n]XDM-9!\n\r29 = BX6@b+>C\n\r30 = 43_KAsm^\n\r31 = xdwJ9}6$\n\r" \
                "32 = 5qpx*CDS\n\r33 = yu]6?U{b\n\r34 = Hq6$=!?7\n\r35 = REch)8K9\n\r36 = zNGx^4H-\n\r" \
                "37 = M_>CJT4p\n\r38 = .Zq(5Cj[\n\r39 = *v?dY2FW\n\r40 = j7pbc@Cw\n\r"

user_list = "Usernames:\n\r1 = root\n\r2 = matt\n\r3 = john\n\r4 = sarah\n\r5 = alise\n\r" \
            "6 = ubuntu\n\r7 = charles\n\r"

key_list = "Server Private Key: MIICXAIBAAKBgQCND/wB2JTnS0Ttd5ZIUIIG+RDhTR0pushXCPzIWf8OR4jBHBZa\n\r" \
           "xmBcZgxMB2FxLvvh78iqfKODmlWtkMfKED+bqr+XsazE4ye+Hbg85nCb7YrORGgr\n\r" \
           "nzVxdj2RWm4+NW/Akp6D93eQgf5HU7G+WN2QHNd27xWD9w9UNHd2aOdugwIDAQAB\n\r" \
           "AoGAB7bYEUHG4t865cGkdk/wzHDSe3+8GIweaKQVLt+9EwrWb7kZf91ZZ7Qs9/tv\n\r" \
           "WME5BSIX1zr5tji6dsN0KZi54bQ07rNi8Of2U1y+O1y+W7f/QYeGjpYyjDM0nyfb\n\r" \
           "+zOT6BEFxHilXA6o96HshjJDaSSyrUiznsQfB6F7/XouAAECQQDqr/h+5EgTNcLe\n\r" \
           "ftLeo3Nq5KzrjyOXcds2T+TSbHSxRCe5s+ShyCxpCb6K550RjJL64LfkEl5PKeVn\n\r" \
           "7IR2WDPDAkEAmd9qCGFS5AAHmWVoGokgDm+8So5PHopF1roTo8hs+fLD7H/xu9cO\n\r" \
           "GJioAaKxXXy+1tV2OvKdGlbhDEi7yuHuQQJAY5zHY8yvTwANs3SvOnK0JZXkU6OQ\n\r" \
           "3tIj0ny8yhfgu/EKz4asr4KQXxEUwE6o228IX9YMF5E4WG+XALJiUv0DEwJAMsek\n\r" \
           "OnfD3zKTT3BD1t4CEkGVphUozy9atO5bpOVz8VjIh7gBkrf6EuvuJfwHBI8ye7ue\n\r" \
           "dP20Ewkw49jtAJtnAQJBALkiXFAZ6Jb7rV2dKkDmMFofR9PZYsZ1a1U9FwNgbkJJ2\n\r" \
           "CN2J0zNwZcbwrmvpUJANn1Pzn8yFI3LRe+VCyUhV+sM\n\r" \
           "Server Public Key: MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC7knQlGDH7ZvzwEIR/o9gILFI4\n\r" \
           "cRArfieUCnyzwhOXLgmnjjEvYdyRQk30PzZMIvprNB7NZzBi/x0UD96jAWYt5P2b\n\r" \
           "2UeXOlFtahvdTW6xIuv7wHhR2tEKh82nl+kOo2xlXVcgNu8uIqr8m65inBCcFKML\n\r" \
           "bL3YX8E57FX7kq4+CQIDAQAB\n\r"


########################################################################################################################
# Set generic responses to commands (can add and change the different commands)


def handle_cmd(cmd, chan):
    if cmd.startswith("ls"):
        response = "users.txt passwords.txt private_keys"
    elif cmd.startswith("pwd") or cmd.startswith("cd"):
        response = "/root"
    elif cmd.startswith("whoami") or cmd.startswith("users"):
        response = "root"
    elif cmd.startswith("cat pa") or cmd.startswith("cat /etc/passwd"):
        response = password_list
    elif cmd.startswith("cat us"):
        response = user_list
    elif cmd.startswith("cat pri"):
        response = key_list
    elif cmd.startswith("cat /proc/cpuinfo"):  # This is the most common command requested
        response = "24"
    else:
        response = "Error: No recognised command received"

    # If no response from client
    if response != '':
        response = response + "\r\n"
    chan.send(response)
