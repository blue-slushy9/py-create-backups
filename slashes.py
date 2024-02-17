oper_sys = input("Are you on Windows, macOS, or Linux?\n")
oper_sys = oper_sys.lower()
if oper_sys == "windows":
    slashes = "\\"
else:
    slashes = "/"
    #return slashes
# DEBUG
print(slashes)