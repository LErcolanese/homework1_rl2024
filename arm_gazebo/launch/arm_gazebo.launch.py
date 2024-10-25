from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    

    other_launch_file_arm_world = PathJoinSubstitution(
        [FindPackageShare("arm_gazebo"), "launch", "arm_world.launch.py"]
    )

    
    include_other_launch_arm_world= IncludeLaunchDescription(
        PythonLaunchDescriptionSource(other_launch_file_arm_world)
    )

    other_launch_file_arm_control= PathJoinSubstitution(
        [FindPackageShare("arm_control"), "launch", "arm_control.launch.py"]
    )

    
    include_other_launch_arm_control = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(other_launch_file_arm_control)
    )

    
    return LaunchDescription([
        include_other_launch_arm_world, 
        include_other_launch_arm_control

    ])
