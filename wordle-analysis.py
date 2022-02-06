import time
start_time = time.time()

with open("accepted-words.csv", "r") as f:
    accepted = f.readline()
with open("answer-words.csv", "r") as f:
    answers = f.readline()

accepted = accepted.split(",")
answers = answers.split(",")

csv_rows = []

for word in accepted:
    score = 0
    # Iterate each character in the word    
    for char in range(0,5):
        for w in answers:
            if w[char] == word[char]:
                score += 1 # Add to the score if the word has a character in the right place
                
    csv_rows.append(f"{word},{score}\n")
    print(csv_rows[-1])

with open("results.csv", "w") as f:
    f.writelines(csv_rows)

print("Collected results in %s seconds" % (time.time() - start_time))