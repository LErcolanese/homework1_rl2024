from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import os
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
)
 

def generate_launch_description():

    declared_arguments = [] 
 
    declared_arguments.append(
        DeclareLaunchArgument(
            "rviz_config_file", #this will be the name of the argument  
            default_value=PathJoinSubstitution(
                [FindPackageShare("arm_description"), "config", "rviz", "arm.rviz"]
            ),
            description="RViz config file (absolute path) to use when launching rviz.",
        )
    )


    arm_path = get_package_share_directory('arm_description')

    arm_urdf = os.path.join(arm_path, "urdf", "arm.urdf")
    desc_path_xacro=os.path.join(arm_path, "urdf", "arm.urdf.xacro")


    with open(arm_urdf, 'r') as info:
        arm_desc = info.read()

    robot_arm_description = {"robot_description": arm_desc}
    r_d_x = {"robot_description":Command(['xacro ', desc_path_xacro])}


    joint_state_publisher_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
    )  

    robot_state_publisher_node_links = Node(
        package="robot_state_publisher", #ros2 run robot_state_publisher robot_state_publisher
        executable="robot_state_publisher",
        output="both",
        parameters=[r_d_x,
                    {"use_sim_time": True},
            ],
        remappings=[('/robot_description', '/robot_description')]
    )


    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", LaunchConfiguration("rviz_config_file")],
    )

    nodes_to_start = [
        joint_state_publisher_node,
        robot_state_publisher_node_links,
        rviz_node
    ]
    
    return LaunchDescription(declared_arguments + nodes_to_start) 