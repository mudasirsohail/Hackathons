# Verification Steps for Simulation Examples

## Prerequisites
- Gazebo Garden installed and configured
- Unity 2022.3 LTS or later
- ROS 2 Humble Hawksbill
- Unity Robotics packages installed (ROS# or equivalent)

## Gazebo Robot Model Example (gazebo-robot-model.xml)
1. Make sure your Gazebo environment is set up:
   ```bash
   # Source ROS 2 environment
   source /opt/ros/humble/setup.bash
   ```

2. Launch Gazebo:
   ```bash
   gz sim
   # or for older versions:
   gazebo
   ```

3. Insert the robot model into the simulation:
   - In Gazebo GUI, go to "Insert" tab
   - Select "Models" and choose "Simple Box Robot" (or load your model via file)
   - Or via command line: `gz model -f /path/to/gazebo-robot-model.xml -m simple_box_robot`

4. Verify the robot appears in the simulation with correct physics properties:
   - The robot should have appropriate mass and inertia
   - Collision and visual properties should match the description
   - The robot should respond to gravity and collisions appropriately

## Unity Robot Scene (Conceptual)
1. Open Unity Hub and launch Unity 2022.3 LTS
2. Create a new 3D project or open existing robotics project
3. Import the robot scene or create components as described in unity-robot-scene.txt
4. Verify physics properties:
   - Check that Rigidbody components have correct mass values
   - Confirm PhysicMaterial has appropriate friction values
   - Ensure collision layers are properly configured

5. Run the scene to verify:
   - Robot responds correctly to physics simulation
   - Collisions behave as expected
   - Sensors (if implemented) output appropriate data

## LiDAR Simulation Example (lidar-simulation.cs)
1. In Unity, create a new scene with:
   - A ground plane
   - Some obstacle objects
   - An empty GameObject with the LidarSimulation script attached

2. Attach the script to an empty GameObject:
   - Create an empty GameObject and name it "LiDAR_Sensor"
   - Attach the LidarSimulation.cs script
   - Adjust parameters: numRays, maxDistance, fov as needed

3. Run the simulation:
   - Press Play in Unity
   - The script will now simulate LiDAR readings
   - Check the Gizmos view to see the simulated LiDAR rays

4. Verify output:
   - The Scan() method should return accurate distance measurements
   - Objects within maxDistance should be detected
   - Rays should properly handle collisions with environment objects

## Depth Camera Simulation Example (depth-camera-simulation.cs)
1. Create a new camera in Unity scene or use existing one
2. Attach the DepthCamera.cs script to the camera GameObject
3. Configure the camera settings:
   - Set appropriate field of view
   - Ensure depth texture mode is enabled

4. Run the simulation:
   - Press Play in Unity
   - Check that the texture is being generated properly
   - Verify that GetDepthImage() returns valid depth data

5. Expected results:
   - The camera should output depth information
   - Closer objects should have different values than distant ones
   - Surfaces should be properly detected

## IMU Simulation Example (imu-simulation.cs)
1. Attach the IMUSimulation.cs script to a GameObject with a Rigidbody component
2. Configure the noise and bias parameters as needed
3. Run the simulation and move the GameObject

4. Verify:
   - The script outputs acceleration values that correspond to movement
   - Angular velocity is properly simulated when the object rotates
   - Noise and bias are appropriately simulated

## Expected Results for Success Criteria (SC-002)
- Users can create and simulate a simple robot model in Gazebo with realistic physics behavior
- The simulation should follow physical laws (gravity, collisions, etc.)
- Users should be able to observe realistic robot behavior in the simulation environment
- All code examples should run without errors and produce expected outputs

## Troubleshooting Common Issues
### Gazebo Issues
- If the robot falls through the ground, check collision properties in the world file
- If physics seem unrealistic, verify mass and inertia properties in the model file
- If models don't appear, check that the SDF file is properly formatted

### Unity Issues
- If physics behave unexpectedly, verify that colliders and rigidbodies are properly configured
- If sensors don't update, check that the scripts are attached to appropriate GameObjects
- Ensure Unity's physics settings are configured appropriately for your simulation

### General Verification
- Compare simulated behavior with expected physical behavior
- Validate that robot movements correlate with command inputs
- Ensure sensor outputs are reasonable given the simulated environment