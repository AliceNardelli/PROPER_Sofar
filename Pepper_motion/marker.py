import qi
import argparse
import sys
import time
import threading

detected = False

def marker_detected(value): #esempio di callback
    print(value)
    global detected
    detected=True
    print("detected")
    time.sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="130.251.13.140",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))        
        #app = qi.Application(["TabletModule", "--qi-url=" + "tcp://" + args.ip + ":" + str(args.port)])
        #app.start()
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    mem=session.service("ALMemory")
    det = mem.subscriber("LandmarkDetected") #"MiddleTactilTouched"
    connection = det.signal.connect(marker_detected) #segnale della sottoscrizione
    while detected==False:
            print("while")
            time.sleep(1)