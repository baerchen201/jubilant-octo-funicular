with open("ttycolors-arch.txt", "r") as f:
    reds, greens, blues = f.read().replace(" ","").splitlines()[:3]
    print("Red Grn Blu   Hex")
    for col in zip(reds.split(","), greens.split(","), blues.split(",")):
        print(*[" "*(3-len(i))+i for i in col], "#"+"".join([f"{int(i):0>2x}" for i in col]))

