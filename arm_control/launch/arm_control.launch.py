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
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.actions import TimerAction


def generate_launch_description():
    declared_arguments = []



    joint_state_broadcaster = TimerAction (
        period=10.0,
        actions=[
        Node(
            package="controller_manager",
            executable="spawner",
            arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
        )
        ]
    )

    position_controller = TimerAction (
        period=10.0,
        actions=[
        Node(
            package="controller_manager",
            executable="spawner",
            arguments=["position_controller", "--controller-manager", "/controller_manager"],
        )
        ]
    )


    # #Launch the ros2 controllers after the model spawns in Gazebo 
    # delay_joint_traj_controller = RegisterEventHandler(
    #     event_handler=OnProcessExit(
    #         target_action=gz_spawn_entity,
    #         on_exit=[position_controller],
    #     )
    # )

    # delay_joint_state_broadcaster = (
    #     RegisterEventHandler(
    #         event_handler=OnProcessExit(
    #             target_action=gz_spawn_entity,
    #             on_exit=[joint_state_broadcaster],
    #         )
    #     )
    # )


    nodes_to_start = [
        joint_state_broadcaster,
        position_controller
    ]

    return LaunchDescription(declared_arguments + nodes_to_start) 
