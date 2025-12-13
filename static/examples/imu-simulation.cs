using UnityEngine;

public class IMUSimulation : MonoBehaviour
{
    // IMU properties
    public float noiseMagnitude = 0.01f;
    public float bias = 0.001f;
    
    // Simulated values
    private Vector3 linearAcceleration;
    private Vector3 angularVelocity;
    private Vector3 magneticField;
    
    // For noise generation
    private float noiseOffset;
    
    void Start()
    {
        noiseOffset = Random.Range(0f, 100f);
        linearAcceleration = Vector3.zero;
        angularVelocity = Vector3.zero;
        magneticField = new Vector3(0.2f, 0f, 0.5f); // Approximate Earth's magnetic field
    }
    
    void Update()
    {
        // Get the actual acceleration and rotation from the physics
        Rigidbody rb = GetComponent<Rigidbody>();
        if (rb != null)
        {
            // Convert world acceleration to local IMU frame
            linearAcceleration = transform.InverseTransformDirection(rb.worldAcceleration);
            
            // Get angular velocity from the rigidbody
            angularVelocity = transform.InverseTransformDirection(rb.angularVelocity);
        }
        
        // Add noise and bias to simulate real IMU behavior
        float time = Time.time;
        Vector3 noise = new Vector3(
            Mathf.PerlinNoise(time + noiseOffset, noiseOffset) - 0.5f,
            Mathf.PerlinNoise(noiseOffset, time + noiseOffset) - 0.5f,
            Mathf.PerlinNoise(time + noiseOffset, time + noiseOffset) - 0.5f
        ) * noiseMagnitude;
        
        Vector3 biasVector = new Vector3(bias, bias, bias);
        
        // Apply noise and bias to measurements
        Vector3 noisyLinearAcc = linearAcceleration + noise + biasVector;
        Vector3 noisyAngularVel = angularVelocity + noise + biasVector;
        Vector3 noisyMagneticField = magneticField + noise * 0.1f;  // Magnetic field has less noise
        
        // Publish or store the simulated IMU data
        PublishIMUData(noisyLinearAcc, noisyAngularVel, noisyMagneticField);
    }
    
    void PublishIMUData(Vector3 acc, Vector3 gyro, Vector3 mag)
    {
        // In a real implementation, this would publish data via ROS or another protocol
        // For this example, we'll just store the values
        
        // Example of what would be published in ROS format:
        /*
        sensor_msgs.Imu imuMsg = new sensor_msgs.Imu();
        imuMsg.header.stamp = ros.Timespan.Now();
        imuMsg.header.frame_id = "imu_link";
        
        imuMsg.linear_acceleration = new geometry_msgs.Vector3(acc.x, acc.y, acc.z);
        imuMsg.angular_velocity = new geometry_msgs.Vector3(gyro.x, gyro.y, gyro.z);
        // Orientation would be computed from integration of gyro data
        
        rosPublisher.Publish(imuMsg);
        */
        
        // For demonstration, we can log the values
        Debug.Log($"IMU Data - Acc: {acc}, Gyro: {gyro}");
    }
    
    // Accessor methods for other scripts to get IMU data
    public Vector3 GetLinearAcceleration()
    {
        return linearAcceleration;
    }
    
    public Vector3 GetAngularVelocity()
    {
        return angularVelocity;
    }
    
    public Vector3 GetMagneticField()
    {
        return magneticField;
    }
}