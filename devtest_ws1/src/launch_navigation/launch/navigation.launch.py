from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

from launch_ros.actions import Node



gazebo_launch_path = PathJoinSubstitution(
    [FindPackageShare("articubot_one"), "launch", "gazebo.launch.py"]
)

def generate_launch_description():
    return LaunchDescription([


        # Launch your robot state publisher and Gazebo spawn_entity.py
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(gazebo_launch_path),
            launch_arguments={
                'use_sim_time': 'true'
            }.items(),
        ),

    ])
