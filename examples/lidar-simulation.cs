using UnityEngine;

public class LidarSimulation : MonoBehaviour
{
    public int numRays = 360;
    public float maxDistance = 30.0f;
    public float fov = 360.0f;
    
    [System.Serializable]
    public class LidarHit
    {
        public float angle;
        public float distance;
    }
    
    public LidarHit[] Scan()
    {
        LidarHit[] hits = new LidarHit[numRays];
        
        for (int i = 0; i < numRays; i++)
        {
            float angle = (i * fov / numRays) * Mathf.Deg2Rad;
            Vector3 direction = new Vector3(Mathf.Cos(angle), 0, Mathf.Sin(angle));
            
            hits[i] = new LidarHit();
            hits[i].angle = angle;
            
            if (Physics.Raycast(transform.position, transform.TransformDirection(direction), 
                               out RaycastHit hit, maxDistance))
            {
                hits[i].distance = hit.distance;
            }
            else
            {
                hits[i].distance = maxDistance; // No obstacle detected
            }
        }
        
        return hits;
    }
    
    // For visualization purposes
    void OnDrawGizmosSelected()
    {
        if (numRays <= 0) return;
        
        Gizmos.color = Color.red;
        for (int i = 0; i < numRays; i += 20) // Draw every 20th ray to avoid clutter
        {
            float angle = (i * fov / numRays) * Mathf.Deg2Rad;
            Vector3 direction = new Vector3(Mathf.Cos(angle), 0, Mathf.Sin(angle));
            Gizmos.DrawRay(transform.position, transform.TransformDirection(direction) * maxDistance);
        }
    }
}