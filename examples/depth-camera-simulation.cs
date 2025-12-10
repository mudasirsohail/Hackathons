using UnityEngine;

public class DepthCamera : MonoBehaviour
{
    public RenderTexture depthTexture;
    public Camera cam;
    
    void Start()
    {
        cam = GetComponent<Camera>();
        cam.depthTextureMode = DepthTextureMode.Depth;
        
        depthTexture = new RenderTexture(640, 480, 24);
        cam.targetTexture = depthTexture;
    }
    
    // This function can process the depth texture for output
    public Texture2D GetDepthImage()
    {
        RenderTexture.active = depthTexture;
        Texture2D depthImage = new Texture2D(depthTexture.width, depthTexture.height);
        depthImage.ReadPixels(new Rect(0, 0, depthTexture.width, depthTexture.height), 0, 0);
        depthImage.Apply();
        RenderTexture.active = null;
        
        return depthImage;
    }
    
    // Alternative approach using shader for more accurate depth
    public void SetupDepthShader()
    {
        Shader depthShader = Shader.Find("Custom/DepthOnly");
        if (depthShader != null)
        {
            cam.SetReplacementShader(depthShader, "RenderType");
        }
    }
}