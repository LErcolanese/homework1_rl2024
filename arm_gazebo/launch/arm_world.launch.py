# Copyright 2022 ICube Laboratory, University of Strasbourg
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, RegisterEventHandler
from launch.conditions import IfCondition, UnlessCondition
from launch.event_handlers import OnProcessExit, OnProcessStart
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory
from ament_index_python import get_package_prefix
import os


def generate_launch_description():
    # Declare arguments
    declared_arguments = []
   


    link_description_path = get_package_share_directory('arm_description')

    desc_path = os.path.join(link_description_path, "urdf", "arm.urdf")
    desc_path_xacro=os.path.join(link_description_path, "urdf", "arm.urdf.xacro")

    with open(desc_path, 'r') as infp:
        robot_description_content = infp.read()


    robot_description = {'robot_description': robot_description_content}
    r_d_x = {"robot_description":Command(['xacro ', desc_path_xacro])}

   
    robot_state_pub_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        
        output='both',
        parameters=[r_d_x],
    )
   
  

    declared_arguments.append(DeclareLaunchArgument('gz_args', default_value='-r -v 1 empty.sdf',
                              description='Arguments for gz_sim'),)
    
    gazebo_ignition = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [PathJoinSubstitution([FindPackageShare('ros_gz_sim'),
                                    'launch',
                                    'gz_sim.launch.py'])]),
            launch_arguments={'gz_args': LaunchConfiguration('gz_args')}.items()
    )


    gz_spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=['-topic', 'robot_description',
                   '-name', 'arm',
                   '-allow_renaming', 'true',],
    )
 
    ign = [gazebo_ignition, gz_spawn_entity]

    bridge_camera = Node(
        package='ros_ign_bridge',
        executable='parameter_bridge',
        arguments=[
            '/camera@sensor_msgs/msg/Image@gz.msgs.Image',
            '/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo',
            '--ros-args', 
            '-r', '/camera:=/videocamera',
        ],
        output='screen'
    )
    
    nodes = [
        *ign,
        robot_state_pub_node,
        bridge_camera

    ]

    return LaunchDescription(declared_arguments + nodes)
