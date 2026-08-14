import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def launch_setup(context):
    # Evaluamos los valores reales en texto dentro del contexto de ROS 2 Humble
    use_sim_time_str = LaunchConfiguration('use_sim_time').perform(context).lower()
    headless_str = LaunchConfiguration('headless').perform(context).lower()
    launch_rviz_str = LaunchConfiguration('launch_rviz').perform(context).lower()

    pkg_description = get_package_share_directory('andino_custom_description')
    pkg_gazebo = get_package_share_directory('andino_custom_gazebo')

    launch_description_nodes = []

    # 1. CONTROL DE DUPLICADOS: Si es el ROBOT REAL (use_sim_time es false),
    # encendemos nuestro propio publicador de estado local.
    if use_sim_time_str == 'false':
        robot_state_pub = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(pkg_description, 'launch', 'description.launch.py')),
            launch_arguments={'use_sim_time': 'false'}.items()
        )
        launch_description_nodes.append(robot_state_pub)

    # 2. Servidor Físico (Gazebo Headless)
    if use_sim_time_str == 'true':
        gazebo_sim = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(pkg_gazebo, 'launch', 'gazebo.launch.py')),
            launch_arguments={'use_sim_time': 'true', 'headless': headless_str}.items()
        )
        launch_description_nodes.append(gazebo_sim)

    # 3. INTERFAZ GRÁFICA: Si launch_rviz es true, abrimos la ventana de visualización
    if launch_rviz_str == 'true':
        rviz_node = Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            # Forzamos los parámetros de simulación para que RViz2 use el reloj del puente
            arguments=['--ros-args', '-p', 'use_sim_time:=true'] if use_sim_time_str == 'true' else []
        )
        launch_description_nodes.append(rviz_node)

    return launch_description_nodes


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        DeclareLaunchArgument('headless', default_value='true'),
        DeclareLaunchArgument('launch_rviz', default_value='false', description='Lanza RViz2 si es true.'),
        OpaqueFunction(function=launch_setup)
    ])

