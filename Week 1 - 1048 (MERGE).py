"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    # 1. Create a new list of equal dimensions for the resulting list.
    newlist = [0] * len(line)
    last_merged = False

    # 2. Look for non-zero values, and will copy over to the next available entry of the resulting list.
       
    if len(line) < 2:
        return line

    for entry_index in range(0, len(line)):
        if line[entry_index] != 0:
            for re_index in range(0, len(newlist)):
                if newlist[re_index] == 0:
                    newlist[re_index] = line[entry_index]
                    last_merged = False
                    break
                elif newlist[re_index + 1] == 0:
                    if newlist[re_index] == line[entry_index] and last_merged is False:
                        newlist[re_index] = newlist[re_index] + line[entry_index]
                        last_merged = True
                        break

    return newlist
