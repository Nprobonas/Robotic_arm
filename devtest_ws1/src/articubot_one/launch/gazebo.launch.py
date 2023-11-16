from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

from launch_ros.actions import Node

warehouse_world_path = PathJoinSubstitution(
    [FindPackageShare("articubot_one"), "worlds", "world1.world"]
)

gazebo_path = PathJoinSubstitution(
    [FindPackageShare("gazebo_ros"), "launch", "gazebo.launch.py"]
)

description_launch_path = PathJoinSubstitution(
    [FindPackageShare("articubot_one"), "launch", "rsp.launch.py"]
)

def generate_launch_description():
    return LaunchDescription([
        # Launch Gazebo with GazeboRosFactory
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(gazebo_path),
            launch_arguments={
                'use_sim_time': 'true',
                'world': warehouse_world_path,
                'verbose': 'true'
            }.items(),
        ),

        # Launch your robot state publisher and Gazebo spawn_entity.py
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(description_launch_path),
            launch_arguments={
                'use_sim_time': 'true'
            }.items(),
        ),

        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-topic', 'robot_description', '-entity', 'my_bot'],
            output='log'
        ),

    ])
