# 1. Base oficial estable
FROM ros:humble-ros-base-jammy

# 2. Variables de entorno globales indispensables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
ENV QT_X11_NO_MITSHM=1

WORKDIR /workspace

# 3. Instalación de paquetes del sistema y dependencias de simulación/navegación
RUN apt-get update && apt-get install --no-install-recommends -y \
    ros-humble-ros-gz \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-slam-toolbox \
    ros-humble-andino-description \
    ros-humble-andino-gz \
    ros-humble-xacro \
    ros-humble-rviz2 \
    ros-humble-teleop-twist-keyboard \
    ros-humble-rqt-graph \
    python3-colcon-common-extensions \
    python3-pip \
    git \
    sudo \
    && rm -rf /var/lib/apt/lists/*


# 5. AUTOMATIZACIÓN DE ENTORNO: Inyectar el source de ROS 2 para cualquier sesión interactiva
RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc

# 6. Copiar configuraciones iniciales
COPY src /workspace/src

# 7. Compilación automática: Deja construidos los paquetes antes de que inicie el contenedor
RUN bash -c "source /opt/ros/humble/setup.bash && colcon build --symlink-install"

# 8. Cargar automáticamente tu espacio de trabajo local compilado al abrir una terminal
RUN echo "source /workspace/install/setup.bash" >> /root/.bashrc

ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]
