print("hello")

import sys

# pylint: disable=F0401
import ac
# pylint: disable=F0401
import acsys


sys.path.insert(len(sys.path), 'apps/python/tensortrainer/third_party')

import os
import mmap

appwindow = 0
last_lap_time = 0
speed_meters_s = 0
angular_vel = 0
gas_brake_clutch_handbrake = 0
steer_pos = 0
lap_invalidated = 0
current_lap = 0
last_lap = 0
performance_meter = 0

# Create the file and fill it with line ends
#open file descriptor
fd = os.open('C:\\cygwin64\\home\\Paulito\\git\\acbot\\drive', os.O_CREAT | os.O_TRUNC | os.O_RDWR)
os.write(fd, b'\n' * mmap.PAGESIZE)
 
buf = mmap.mmap(fd, mmap.PAGESIZE, access=mmap.ACCESS_WRITE)






def acMain(ac_version):

    global appwindow, speed_meters_s,angular_vel,gas_brake_clutch_handbrake,steer_pos,lap_invalidated,current_lap,last_lap,performance_meter

    appWindow = ac.newApp("TensorTrainer")
    ac.setSize(appWindow, 200, 200)
    speed_meters_s = ac.addLabel(appWindow, "Speed(M/s): 0")
    angular_vel = ac.addLabel(appWindow, "Ang.Vel.: 0")
    gas_brake_clutch_handbrake = ac.addLabel(appWindow, "GBCH: 0000")
    steer_pos = ac.addLabel(appWindow, "Steer: 0")
    lap_invalidated = ac.addLabel(appWindow, "LapValid: Yes")
    current_lap = ac.addLabel(appWindow, "Current: 0")
    last_lap = ac.addLabel(appWindow, "Last: 0")
    performance_meter = ac.addLabel(appWindow, "Perf: 0")

    ac.setPosition(speed_meters_s, 3, 30)
    ac.setPosition(angular_vel, 3, 45)
    ac.setPosition(gas_brake_clutch_handbrake, 3, 60)
    ac.setPosition(steer_pos, 3, 75)
    ac.setPosition(lap_invalidated, 3, 90)
    ac.setPosition(current_lap, 3, 105)
    ac.setPosition(last_lap, 3, 120)
    ac.setPosition(performance_meter, 3, 135)


    return "TensorTrainer"

def acUpdate(deltaT):

    global speed_meters_s,angular_vel,gas_brake_clutch_handbrake,steer_pos,lap_invalidated,current_lap,last_lap,performance_meter,last_lap_time

    speed = ac.getCarState(0, acsys.CS.SpeedMS)
    ang_vel = ac.getCarState(0,acsys.CS.LocalAngularVelocity)
    gas = ac.getCarState(0, acsys.CS.Gas)
    brake = ac.getCarState(0,acsys.CS.Brake)
    clutch =  ac.getCarState(0, acsys.CS.Clutch)
    #handbrake = ac.getCarState(0, acsys.CS.Handbrake)
    handbrake = 0
    steer = ac.getCarState(0,acsys.CS.Steer)
    lap_valid = ac.getCarState(0,acsys.CS.LapInvalidated)
    currentlap = ac.getCarState(0,acsys.CS.LapTime)
    last = ac.getCarState(0,acsys.CS.LastLap)
    perf = ac.getCarState(0,acsys.CS.PerformanceMeter)

    if last_lap_time != last:
        last_lap_time = last
        ac.setText(last_lap, "Last: {}".format(last))
    valid = "Yes"
    if lap_valid == 0:
        valid = "No"

    ac.setText(lap_invalidated, "LapValid: {}".format(valid))

    ac.setText(speed_meters_s, "Speed(M/s): {}".format(str(speed)[0:4]))

    short_ang = []

    for each in ang_vel:
        short_ang.append('%.3f'%(each))
    ac.setText(angular_vel, "Ang.Vel.: {}".format(str(short_ang)))

    ac.setText(gas_brake_clutch_handbrake, "GBCH: {}".format(['%.3f'%(gas), '%.3f'%(brake), '%.3f'%(clutch), handbrake]))
    ac.setText(steer_pos, "Steer: {}".format(str('%.3f'%(steer))))
    ac.setText(current_lap, "Current: {}".format(currentlap))
    ac.setText(performance_meter, "Perf.: {}".format(perf))

    update_data = [
        '%.3f'%(speed),
        short_ang,
        gas,
        brake,
        clutch,
        handbrake,
        '%.3f'%(steer),
        lap_valid,
        current_lap,
        last,
        perf
    ]

    # try:
    #     out_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     out_socket.connect(("localhost", 86))

    #     send_string = bytes(str(update_data), "UTF-8")
    #     ac.log(send_string)
    #     #push all this data to socket out
    #     out_socket.send(send_string)
    #     out_socket.close()
    # except:
    #     pass #bleh
    update_str = str(update_data)+"\n"
    buf.write(bytes(update_str, "UTF-8"))
    buf.seek(0)

def acShutdown():
    buf.flush()
    buf.write(bytes("stop\n", "UTF-8"))

    