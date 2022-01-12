import time
import os


def read_ids():
    with open("ids.txt") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    content = [x.split(" ")[0] for x in content]
    for word in content:
        if word.startswith("A"):
            content.remove(word)
    print(content)
    return content


def log(text, file_name):
    t = time.localtime()
    current_time = time.strftime("%d.%m.%Y %H:%M:%S", t)
    log_text = str(current_time) + ": " + str(text)
    print(log_text)
    log_to_file(log_text, file_name)


def log_to_file(text, file_name):
    file = open(file_name + ".txt", 'a+')
    file.write(text)
    file.write("\n")
    file.close()


def main():
    log("test", os.path.basename(__file__))


if __name__ == '__main__':
    main()