# -------------------------------------------------------------------------------------------------------
# NEURONRAIN ASFER - Software for Mining Large Datasets
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------------------------------------------
# K.Srinivasan
# NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
# Personal website(research): https://sites.google.com/site/kuja27/
# --------------------------------------------------------------------------------------------------------


# Analytics enabled Drone Mission - Online Shopping Delivery
# ----------------------------------------------------------
# Following static mission plan example from DronecodeSDK has been changed to illustrate dynamic mission
# plan based on analytics:
# Example Drone Mission - https://github.com/Dronecode/DronecodeSDK-Python/blob/master/examples/mission.py
# Drone MissionItem Proto - https://github.com/Dronecode/DronecodeSDK-Proto/blob/a54b353d73ff8d6e36c716b5278990e0f8cb770c/protos/mission/mission.proto

# Disclaimer: This is not compileable, executable code but only a pseudocode and has not been tested on a drone because of lack of it and aviation licensing requirements

#!/usr/bin/env python3

import asyncio

#from dronecode_sdk import connect as dronecode_sdk_connect
from mavsdk import System
#from dronecode_sdk import (MissionItem)
from mavsdk.mission import MissionItem,MissionPlan
from ImageGraph_Keras_Theano import convex_hull
import Streaming_AbstractGenerator


#drone = dronecode_sdk_connect(host="127.0.0.1")
drone = System()

async def run():
    await drone.connect()
    inputf = Streaming_AbstractGenerator.StreamAbsGen(
        "Socket_Streaming", "localhost")
    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state.uuid}")
            break

    
    mission_items = []
    mission_items.append(MissionItem(47.398039859999997,
                                     8.5455725400000002,
                                     25,
                                     10,
                                     True,
                                     float('nan'),
                                     float('nan'),
                                     MissionItem.CameraAction.NONE,
                                     float('nan'),
                                     float('nan')))
    mission_items.append(MissionItem(47.398036222362471,
                                     8.5450146439425509,
                                     25,
                                     10,
                                     True,
                                     float('nan'),
                                     float('nan'),
                                     MissionItem.CameraAction.NONE,
                                     float('nan'),
                                     float('nan')))
    mission_items.append(MissionItem(47.397825620791885,
                                     8.5450092830163271,
                                     25,
                                     10,
                                     True,
                                     float('nan'),
                                     float('nan'),
                                     MissionItem.CameraAction.NONE,
                                     float('nan'),
                                     float('nan')))

    # Dynamic Mission Plan which autopilots the drone based on GIS analytics navigation variables
    # - e.g. longitude, latitude, altitude, speed, camera action etc., -
    # read by Streaming Abstract Generator socket streaming and appends MissionItems to
    # flight plan dynamically restricted by ordinates convex hull. When drone is within
    # convex hull airspace, its altitude is set to 0 (or minimal value) and landed
    convex_hull_longlats = tolonglat(convex_hull(
        "../../image_pattern_mining/ImageNet/testlogs/SEDAC_GIS_ChennaiMetropolitanArea.jpg"))
    variables_read=False
    longitude = latitude = relative_altitude_m =  speed_m_s = is_fly_through =  gimbal_pitch_deg = gimbal_yaw_deg = camera_action = loiter_time_s = camera_photo_interval_s = 0 
    for gis_analytics_kv_binary in inputf:
        gis_analytics_kv_lines=str(gis_analytics_kv_binary).split("\\n")
        for gis_analytics_kv in gis_analytics_kv_lines:
            gis_analytics_kv_tok=str(gis_analytics_kv).split("=")
            if 'longitude' in str(gis_analytics_kv_tok[0]).strip():
                longitude = float(str(gis_analytics_kv_tok[1]).strip())
                print(longitude)
            if 'latitude' in str(gis_analytics_kv_tok[0]).strip():
                latitude = float(str(gis_analytics_kv_tok[1]).strip())
                print(latitude)
            if 'relative_altitude_m' in str(gis_analytics_kv_tok[0]).strip():
                relative_altitude_m = int(str(gis_analytics_kv_tok[1]).strip()) + 25
                print(relative_altitude_m)
            if 'speed_m_s' in str(gis_analytics_kv_tok[0]).strip():
                speed_m_s = int(str(gis_analytics_kv_tok[1]).strip()) + 10
                print(speed_m_s)
            #if gis_analytics_kv_tok[0] == "is_fly_through":
            #    is_fly_through = gis_analytics_kv_tok[1]
            #    if is_fly_through == "True":
            #        is_fly_through = True
            #    else:
            #        is_fly_through = False
            #if gis_analytics_kv_tok[0] == "gimbal_pitch_deg":
            #    gimbal_pitch_deg = float(gis_analytics_kv_tok[1])
            #if gis_analytics_kv_tok[0] == "gimbal_yaw_deg":
            #    gimbal_yaw_deg = float(gis_analytics_kv_tok[1])
            #if gis_analytics_kv_tok[0] == "camera_action":
            #    if gis_analytics_kv_tok[1] == "1":
            #        camera_action =  MissionItem.CameraAction.TAKE_PHOTO
            #    else:
            #        camera_action =  MissionItem.CameraAction.NONE
            #if gis_analytics_kv_tok[0] == "loiter_time_s":
            #    loiter_time_s = float(gis_analytics_kv_tok[1])
            #if gis_analytics_kv_tok[0] == "camera_photo_interval_s":
            #    camera_photo_interval_s = float(gis_analytics_kv_tok[1])
            if str(gis_analytics_kv)=="end":
                variables_read=True 
                break
        if variables_read:
            break
    if (longitude, latitude) not in convex_hull_longlats:
            print("Outside convex hull: GIS Analytics Variables Read...Mission Items being appended...")
            mission_items.append(MissionItem(longitude,
                                             latitude,
                                             relative_altitude_m,
                                             speed_m_s,
                                             True,
                                             float('nan'),
                                             float('nan'),
                                             MissionItem.CameraAction.NONE,
                                             float('nan'),
                                             float('nan')))
    else:
            print("Inside convex hull: GIS Analytics Variables Read...Mission Items being appended...")
            mission_items.append(MissionItem(longitude,
                                             latitude,
                                             0.0,
                                             0.0,
                                             True,
                                             float('nan'),
                                             float('nan'),
                                             MissionItem.CameraAction.NONE,
                                             float('nan'),
                                             float('nan')))

    print("-- Uploading mission")
    mission_plan=MissionPlan(mission_items)
    await drone.mission.set_return_to_launch_after_mission(True)
    await drone.mission.upload_mission(mission_plan)
    
    print("-- Arming")
    await drone.action.arm()

    print("-- Vertical Takeoff")
    await drone.action.takeoff()

    print("-- Starting mission")
    await drone.mission.start_mission()

    print("-- Taking photo")
    if camera_action == MissionItem.CameraAction.TAKE_PHOTO:
        try:
            drone.camera.take_photo()
        except CameraError:
            print("Camera Error")
    #await asyncio.ensure_future(print_mission_progress())
    #await asyncio.ensure_future(observe_is_in_air())

async def print_mission_progress():
    await drone.connect()
    async for mission_progress in drone.mission.mission_progress():
        #print(f"Mission progress: {mission_progress.current_item_index}/{mission_progress.mission_count}")
        print(f"Mission progress: {mission_progress.current}/{mission_progress.total}")


async def observe_is_in_air():
    """ Monitors whether the drone is flying or not and
    returns after landing """

    await drone.connect()
    was_in_air = False

    async for is_in_air in drone.telemetry.in_air():
        if is_in_air:
            was_in_air = is_in_air

        if was_in_air and not is_in_air:
            await asyncio.get_event_loop().shutdown_asyncgens()
            return


def tolonglat(convexhull):
    # hardcoded
    return [(11, 11),(12, 12),(78, 7)]

def setup_tasks():
    asyncio.ensure_future(run())
    #asyncio.ensure_future(print_mission_progress())


if __name__ == "__main__":
    setup_tasks()
    asyncio.get_event_loop().run_until_complete(observe_is_in_air())
