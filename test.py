import requests

def main():
    json = {}
    json["action"] = "ROOM_NEW"
    json["room_new"] = {}
    json["room_new"]["game"] = "game22"
    json["room_new"]["player"] = "messbees"
    print(json)
    print("Sending your {} request...".format(json["action"]))
    print(requests.post('http://159.100.247.47:8888', json=json))

if __name__ == "__main__":
    main()
