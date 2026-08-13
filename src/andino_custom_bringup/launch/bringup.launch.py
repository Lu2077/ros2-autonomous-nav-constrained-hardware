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
    launch_rviz = LaunchConfiguration('launch_rviz').perform(context)

    pkg_description = get_package_share_directory('andino_custom_description')
    pkg_gazebo = get_package_share_directory('andino_custom_gazebo')
    pkg_bringup = get_package_share_directory('andino_custom_bringup')

    launch_description_nodes = []

    # 1. Modelo estructural del robot
    robot_state_pub = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_description, 'launch', 'description.launch.py')),
        launch_arguments={'use_sim_time': use_sim_time}.items()
    )
    launch_description_nodes.append(robot_state_pub)

    # 2. Servidor Físico (Solo si estamos simulando)
    if use_sim_time.perform(context).lower() == 'true':
        gazebo_sim = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(pkg_gazebo, 'launch', 'gazebo.launch.py')),
            launch_arguments={'use_sim_time': use_sim_time, 'headless': headless_val}.items()
        )
        launch_description_nodes.append(gazebo_sim)

    # 3. Lanzar la interfaz de RViz2 (Opcional - Corre en el front-end de desarrollo)
    if launch_rviz.lower() == 'true':
        # Buscamos si existe un archivo .rviz personalizado, de lo contrario abre uno por defecto
        rviz_config_file = os.path.join(pkg_description, 'rviz', 'andino.rviz')

        rviz_node = Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_config_file] if os.path.exists(rviz_config_file) else [],
            parameters=[{'use_sim_time': use_sim_time}]
        )
        launch_description_nodes.append(rviz_node)

    return launch_description_nodes


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        DeclareLaunchArgument('headless', default_value='true'),
        DeclareLaunchArgument('launch_rviz', default_value='false',
                              description='Lanza la interfaz gráfica de RViz2 si es True.'),
        OpaqueFunction(function=launch_setup)
    ])

