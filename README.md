**ROS2 Autonomous Navigation on Constrained Hardware**

*A lightweight, containerized development framework for deploying ROS2 autonomous navigation projects on resource-constrained hardware. This project separates heavy physics simulations from frontend visualization to enable efficient development on low-performance computers.* 

**🎯 Project Objective**

*To provide a streamlined environment for developing and testing ROS2 navigation stacks on hardware with limited computational resources. By decoupling the simulation backend from the visualization frontend into separate containers, this architecture minimizes memory footprint and CPU usage while maintaining full simulation fidelity.* 

🏗️ Architecture Overview

**The system utilizes a microservices-based approach with two distinct Docker containers:**

*Backend Container:*
Runs Gazebo Ignition Fortress in headless server mode (ign gazebo -s).  It handles heavy physics calculations, world simulation (world.sdf), and LiDAR data generation without GUI overhead.

*Frontend Container:* 
Runs RViz2 for lightweight 3D visualization and rendering. It subscribes to sensor topics from the backend, allowing developers to monitor robot behavior without running the full simulation stack locally. 
This separation allows the heavy simulation to run on a remote server or a dedicated backend instance, while the frontend can operate on a low-spec laptop or embedded device.
