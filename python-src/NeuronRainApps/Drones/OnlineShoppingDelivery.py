#-------------------------------------------------------------------------------------------------------
#NEURONRAIN ASFER - Software for Mining Large Datasets
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#--------------------------------------------------------------------------------------------------------
#K.Srinivasan
#NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
#Personal website(research): https://sites.google.com/site/kuja27/
#--------------------------------------------------------------------------------------------------------


#Analytics enabled Drone Mission - Online Shopping Delivery
#----------------------------------------------------------
#Following static mission plan example from DronecodeSDK has been changed to illustrate dynamic mission 
#plan based on analytics:
#Example Drone Mission - https://github.com/Dronecode/DronecodeSDK-Python/blob/master/examples/mission.py
#Drone MissionItem Proto - https://github.com/Dronecode/DronecodeSDK-Proto/blob/a54b353d73ff8d6e36c716b5278990e0f8cb770c/protos/mission/mission.proto

#Disclaimer: This is not compileable, executable code but only a pseudocode and has not been tested on a drone because of lack of it and aviation licensing requirements

#!/usr/bin/env python3

import asyncio

from dronecode_sdk import connect as dronecode_sdk_connect
from dronecode_sdk import (MissionItem)
from ImageGraph_Keras_Theano import convex_hull


drone = dronecode_sdk_connect(host="127.0.0.1")


async def run():
    inputf=Streaming_AbstractGenerator.StreamAbsGen("Socket_Streaming","localhost")
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

    #Dynamic Mission Plan which autopilots the drone based on GIS analytics navigation variables 
    # - e.g. longitude, latitude, altitude, speed, camera action etc., -
    #read by Streaming Abstract Generator socket streaming and appends MissionItems to
    #flight plan dynamically restricted by ordinates convex hull. When drone is within 
    #convex hull airspace, its altitude is set to 0 (or minimal value) and landed
    convex_hull_longlats=tolonglat(convex_hull("testlogs/SEDAC_GIS_ChennaiMetropolitanArea.jpg"))
    for gis_analytics in inputf:
    	longitude=gis_analytics[0]
    	latitude=gis_analytics[1]
    	relative_altitude_m=gis_analytics[2]
    	speed_m_s=gis_analytics[3]
    	is_fly_through=gis_analytics[4]
    	gimbal_pitch_deg=gis_analytics[5]
    	gimbal_yaw_deg=gis_analytics[6]
    	camera_action=gis_analytics[7]
	if camera_action==TAKE_PHOTO:
		try:
			drone.camera.take_photo()
		except CameraError:
			print "Camera Error"
    	loiter_time_s=gis_analytics[8]
    	camera_photo_interval_s=gis_analytics[9]
    
	if (longitude,latitude) not in convex_hull_longlats:
    		mission_items.append(MissionItem(longitude,
		latitude,
		relative_altitude_m,
		speed_m_s,
		is_fly_through,
		gimbal_pitch_deg,
		gimbal_yaw_deg,
		camera_action,
		loiter_time_s,
    		camera_photo_interval_s))
	else:
		mission_items.append(MissionItem(longitude,
		latitude,
		0,
		0,
		is_fly_through,
		gimbal_pitch_deg,
		gimbal_yaw_deg,
		camera_action,
		loiter_time_s,
    		camera_photo_interval_s))


    await drone.mission.set_return_to_launch_after_mission(True)

    print("-- Uploading mission")
    await drone.mission.upload_mission(mission_items)

    print("-- Arming")
    await drone.action.arm()

    print("-- Starting mission")
    await drone.mission.start_mission()


async def print_mission_progress():
    async for mission_progress in drone.mission.mission_progress():
        print(f"Mission progress: {mission_progress.current_item_index}/{mission_progress.mission_count}")


async def observe_is_in_air():
    """ Monitors whether the drone is flying or not and
    returns after landing """

    was_in_air = False

    async for is_in_air in drone.telemetry.in_air():
        if is_in_air:
            was_in_air = is_in_air

        if was_in_air and not is_in_air:
            await asyncio.get_event_loop().shutdown_asyncgens()
            return

def tolonglat(convexhull):
    #hardcoded
    return [(11,11),(12,12),(78,07)]

def setup_tasks():
    asyncio.ensure_future(run())
    asyncio.ensure_future(print_mission_progress())


if __name__ == "__main__":
    setup_tasks()
    asyncio.get_event_loop().run_until_complete(observe_is_in_air())
