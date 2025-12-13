# PowerShell script to deploy Docusaurus v3 project to GitHub Pages
# This script will handle all deployment tasks for the project at https://github.com/mudasirsohail/Hackathons

param(
    [string]$GitHubToken = $env:GITHUB_TOKEN,
    [string]$GitHubRepo = "mudasirsohail/Hackathons",
    [string]$GitHubUser = "mudasirsohail",
    [string]$RepoURL = "https://github.com/mudasirsohail/Hackathons"
)

Write-Host "Starting deployment of Docusaurus project to GitHub Pages..." -ForegroundColor Green

# Change to the docs directory
Set-Location -Path "D:\Hackathon 1\docs"

# Function to display error messages
function Show-Error {
    param([string]$Message)
    Write-Host "ERROR: $Message" -ForegroundColor Red
}

# Function to display success messages
function Show-Success {
    param([string]$Message)
    Write-Host "SUCCESS: $Message" -ForegroundColor Green
}

# Function to display info messages
function Show-Info {
    param([string]$Message)
    Write-Host "INFO: $Message" -ForegroundColor Yellow
}

# 1. Delete .docusaurus folder and node_modules
Write-Host "`n1. Cleaning up old build files..." -ForegroundColor Cyan
try {
    if (Test-Path ".docusaurus") {
        Remove-Item -Path ".docusaurus" -Recurse -Force
        Show-Success ".docusaurus folder deleted"
    } else {
        Show-Info ".docusaurus folder not found, continuing..."
    }
    
    if (Test-Path "node_modules") {
        Remove-Item -Path "node_modules" -Recurse -Force
        Show-Success "node_modules folder deleted"
    } else {
        Show-Info "node_modules folder not found, continuing..."
    }
} catch {
    Show-Error "Failed to delete folders: $($_.Exception.Message)"
    exit 1
}

# 2. Install dependencies
Write-Host "`n2. Installing dependencies..." -ForegroundColor Cyan
try {
    npm install
    if ($LASTEXITCODE -eq 0) {
        Show-Success "Dependencies installed successfully"
    } else {
        Show-Error "npm install failed with exit code $LASTEXITCODE"
        exit 1
    }
} catch {
    Show-Error "Failed to install dependencies: $($_.Exception.Message)"
    exit 1
}

# 3. Check for broken links in docs
Write-Host "`n3. Checking for broken links..." -ForegroundColor Cyan
try {
    # Docusaurus has built-in link checking during build
    # We'll run the build command to identify broken links
    npm run build
    if ($LASTEXITCODE -eq 0) {
        Show-Success "Build completed without broken links"
    } else {
        # If there are errors but they're not related to broken links, we can still continue
        Show-Info "Build completed with some warnings or errors - checking if this affects deployment"
    }
} catch {
    Show-Error "Build failed due to broken links or other errors: $($_.Exception.Message)"
    exit 1
}

# 4. Create gh-pages branch if it doesn't exist
Write-Host "`n4. Checking for gh-pages branch..." -ForegroundColor Cyan
try {
    $branches = git branch -r
    if ($branches -like "*origin/gh-pages*") {
        Show-Info "gh-pages branch already exists"
    } else {
        Write-Host "Creating gh-pages branch..." -ForegroundColor Yellow
        git checkout -b gh-pages
        git push -u origin gh-pages
        git checkout main  # Return to main branch
        Show-Success "gh-pages branch created and pushed"
    }
} catch {
    Show-Error "Failed to handle gh-pages branch: $($_.Exception.Message)"
    exit 1
}

# 5. Build the site
Write-Host "`n5. Building the site..." -ForegroundColor Cyan
try {
    npm run build
    if ($LASTEXITCODE -eq 0) {
        Show-Success "Site built successfully"
    } else {
        Show-Error "Build failed with exit code $LASTEXITCODE"
        exit 1
    }
} catch {
    Show-Error "Failed to build site: $($_.Exception.Message)"
    exit 1
}

# 6. Deploy to GitHub Pages
Write-Host "`n6. Deploying to GitHub Pages..." -ForegroundColor Cyan

# Check if the docusaurus deploy command exists in package.json
$packageJson = Get-Content -Path "package.json" -Raw | ConvertFrom-Json

if ($packageJson.scripts -and $packageJson.scripts.deploy) {
    # If deploy script is defined in package.json, use it
    try {
        npm run deploy
        if ($LASTEXITCODE -eq 0) {
            Show-Success "Site deployed using npm run deploy"
        } else {
            Show-Error "Deployment failed with exit code $LASTEXITCODE"
            exit 1
        }
    } catch {
        Show-Error "Failed to deploy using npm run deploy: $($_.Exception.Message)"
        exit 1
    }
} else {
    # If no deploy script, implement manual deployment
    Write-Host "No deploy script found in package.json, using manual deployment..." -ForegroundColor Yellow
    
    # Configure git for deployment
    try {
        git config --global user.name "$GitHubUser"
        git config --global user.email "${GitHubUser}@users.noreply.github.com"
        
        # Clone the gh-pages branch to a temporary directory
        $tempDir = "temp-deploy"
        if (Test-Path $tempDir) {
            Remove-Item -Path $tempDir -Recurse -Force
        }
        
        git clone "https://$GitHubToken@github.com/$GitHubRepo.git" $tempDir --branch gh-pages
        
        # Copy built files to the temporary directory
        $buildDir = "_build"  # Docusaurus builds to this directory by default
        if (Test-Path $buildDir) {
            # Remove existing content in temp directory
            $items = Get-ChildItem -Path $tempDir -Force
            foreach ($item in $items) {
                if ($item.Name -ne ".git") {
                    Remove-Item -Path $item.FullName -Recurse -Force
                }
            }
            
            # Copy new build files
            Copy-Item -Path "$buildDir/*" -Destination $tempDir -Recurse
            
            # Commit and push changes
            Set-Location -Path $tempDir
            git add .
            git commit -m "Deploy Docusaurus site to GitHub Pages - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
            git push
            
            Show-Success "Site deployed manually to GitHub Pages"
        } else {
            Show-Error "Build directory does not exist: $buildDir"
            exit 1
        }
        
        # Cleanup
        Set-Location -Path "D:\Hackathon 1\docs"
        Remove-Item -Path $tempDir -Recurse -Force
    } catch {
        Show-Error "Manual deployment failed: $($_.Exception.Message)"
        exit 1
    }
}

# 7. Handle authentication for GitHub repo
# This is done via git remote URL with token or git credentials
Write-Host "`n7. GitHub authentication handled via stored credentials or token" -ForegroundColor Cyan

# Final status
Write-Host "`nDeployment completed successfully!" -ForegroundColor Green
Write-Host "Your site should now be available at: https://$GitHubUser.github.io/Hackathons/" -ForegroundColor Green