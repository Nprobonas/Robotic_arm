
import os
import launch_ros
from launch import LaunchDescription
from launch import LaunchContext
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition
from launch.substitutions import EnvironmentVariable
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
import launch_ros.actions
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # slam_launch_path = PathJoinSubstitution(
    #     [FindPackageShare('slam_toolbox'), 'launch', 'online_async_launch.py']
    # )

    # slam_config_path = PathJoinSubstitution(
    #     [FindPackageShare('launch_navigation'), 'config', 'sim_slam.yaml']
    # )

    rviz_config_path = PathJoinSubstitution(
        [FindPackageShare('launch_navigation'), 'rviz', 'slam.rviz']
    )

    filter_config_path = PathJoinSubstitution(
        [FindPackageShare('launch_navigation'), 'config', 'range_filter.yaml']
    )



    rf2o_launch_path = PathJoinSubstitution(
        [FindPackageShare('rf2o_laser_odometry'), 'launch', 'rf2o_laser_odometry.launch.py']
    )    
    

    return LaunchDescription([
        DeclareLaunchArgument(
            name='sim', 
            default_value='false',
            description='Enable use_sime_time to true'
        ),

        DeclareLaunchArgument(
            name='rviz', 
            default_value='false',
            description='Run rviz'
        ),



        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource(rf2o_launch_path),
        # ),

        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource(slam_launch_path),
        #     launch_arguments={
        #         'use_sim_time': LaunchConfiguration("sim"),
        #         'slam_params_file': slam_config_path
        #     }.items()
        # ),

        launch_ros.actions.Node(
          parameters=[
            get_package_share_directory("launch_navigation") + '/config/mapper_params_offline.yaml'
          ],
          package='slam_toolbox',
          executable='sync_slam_toolbox_node',
          name='slam_toolbox',
          output='screen'
        ),

        Node(
            package="laser_filters",
            executable="scan_to_scan_filter_chain",
            parameters=[filter_config_path],
           
        ),


        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_config_path],
            condition=IfCondition(LaunchConfiguration("rviz")),
            parameters=[{'use_sim_time': LaunchConfiguration("sim")}]
        )


    ])
