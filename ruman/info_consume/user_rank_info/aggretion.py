# -*-coding:utf-8-*-

def main():
    with open("social_sensors.txt", "rb") as f:
        uid_set = set()
        for line in f:
            uid = line.strip()
            uid_set.add(uid)

    with open("group.txt", "wb") as f:
        for uid in uid_set:
            f.write(str(uid)+"\n")

if __name__ == "__main__":
    main()
