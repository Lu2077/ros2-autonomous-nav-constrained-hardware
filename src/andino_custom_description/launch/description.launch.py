import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
# 1. IMPORTANTE: Importamos la herramienta de descripción de parámetros para Humble
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    pkg_custom_description = get_package_share_directory('andino_custom_description')
    use_sim_time = LaunchConfiguration('use_sim_time')

    xacro_file = os.path.join(pkg_custom_description, 'urdf', 'andino_custom.urdf.xacro')

    # 2. Procesamos el Xacro con el comando tradicional
    robot_description_raw = Command(['xacro ', xacro_file])

    # 3. CORRECCIÓN CRUCIAL: Envolvemos el resultado diciéndole explícitamente a ROS 2 que es un String puro
    robot_description_formatted = ParameterValue(robot_description_raw, value_type=str)

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'robot_description': robot_description_formatted # <-- Pasamos el parámetro formateado
        }]
    )

    #joint_state_publisher_node = Node(
    #    package='joint_state_publisher',
    #    executable='joint_state_publisher',
    #    name='joint_state_publisher',
    #    output='screen',
    #    parameters=[{'use_sim_time': use_sim_time}]
    #)

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Usa el reloj de la simulación (Gazebo) si es True.'
        ),
        robot_state_publisher_node
        #joint_state_publisher_node
    ])

