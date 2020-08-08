import os
import glob


# This in built to count how many lines of code I have built
# Will be removed when testing and building is finished.
total_lines = 0
pwd = os.getcwd()
chapter_one_files = glob.glob(os.path.join(pwd, "Chapter_One/*.py"))
chapter_two_files = glob.glob(os.path.join(pwd, "Chapter_Two/*.py"))
main_file = os.path.join(pwd, "Vern_Adventures.py")

with open(main_file, "r") as file:
    print(f"Checking {os.path.basename(main_file)}")
    total_lines += len(file.readlines())

for sub_file in chapter_one_files:
    with open(sub_file, "r") as file:
        print(f"Checking {os.path.basename(sub_file)}")
        total_lines += len(file.readlines())

for sub_file in chapter_two_files:
    with open(sub_file, "r") as file:
        print(f"Checking {os.path.basename(sub_file)}")
        total_lines += len(file.readlines())

print(f"The total lines are, {total_lines}")
