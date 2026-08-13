import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def launch_setup(context):
    use_sim_time = LaunchConfiguration('use_sim_time')
    headless_val = LaunchConfiguration('headless').perform(context)

    pkg_custom_gazebo = get_package_share_directory('andino_custom_gazebo')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    world_file = os.path.join(pkg_custom_gazebo, 'worlds', 'andino_world.sdf')

    # Si es headless, combinamos -s (server) y -r (run/reproducir física de inmediato)
    # Si no es headless, usamos -r estándar para la interfaz gráfica activa
    gz_flag = '-s -r' if headless_val.lower() == 'true' else '-r'
    full_gz_args = f"{gz_flag} {world_file}"

    # 1. Servidor de Gazebo (Arranca reproduciendo la física gracias a -r)
    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': full_gz_args}.items()
    )

    # 2. Nodo de Spawn
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        name='spawn_andino',
        output='screen',
        arguments=['-topic', 'robot_description', '-name', 'andino', '-z', '0.1'],
        parameters=[{'use_sim_time': use_sim_time}]
    )

    # 3. Puente de datos (ros_gz_bridge)
    # 3. Puente de datos (ros_gz_bridge) ULTRA-OPTIMIZADO mediante YAML
    parameter_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'config_file': os.path.join(pkg_custom_gazebo, 'config', 'ros_gz_bridge.yaml')  # <-- Carga limpia
        }]
    )

    # Retornamos UNICAMENTE los procesos estables. Eliminamos delayed_unpause de raíz.
    return [
        gazebo_server,
        spawn_robot,
        parameter_bridge
    ]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        DeclareLaunchArgument('headless', default_value='true'),
        OpaqueFunction(function=launch_setup)
    ])
