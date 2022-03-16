def plural(n):
    if n == 1:
        pl = "st"
    elif n == 2:
        pl = "nd"
    elif n == 3:
        pl = "rd"
    else:
        pl = "th"
    return f"{n}{pl}"
