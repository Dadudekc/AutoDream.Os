# V2_SWARM Container Orchestration Deployment Script (PowerShell)
# Deploys the complete containerized V2_SWARM system

param(
    [Parameter(Position=0)]
    [ValidateSet("deploy", "cleanup", "status", "help")]
    [string]$Command = "deploy",

    [string]$Registry = "localhost:5000",
    [string]$ImageTag = "latest"
)

# Configuration
$NAMESPACE = "swarm-system"
$IMAGE_NAME = "swarm-agent-cellphone"

# Functions
function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Check prerequisites
function Test-Prerequisites {
    Write-Info "Checking prerequisites..."

    # Check if kubectl is installed
    if (-not (Get-Command kubectl -ErrorAction SilentlyContinue)) {
        Write-Error "kubectl is not installed. Please install kubectl first."
        exit 1
    }

    # Check if docker is installed
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
        Write-Error "Docker is not installed. Please install Docker first."
        exit 1
    }

    # Check kubectl connection
    try {
        kubectl cluster-info | Out-Null
    }
    catch {
        Write-Error "Cannot connect to Kubernetes cluster. Please check your kubeconfig."
        exit 1
    }

    Write-Success "Prerequisites check passed"
}

# Build Docker image
function Build-Image {
    Write-Info "Building Docker image..."

    docker build -t "${IMAGE_NAME}:${ImageTag}" .

    if ($LASTEXITCODE -eq 0) {
        Write-Success "Docker image built successfully"
    }
    else {
        Write-Error "Failed to build Docker image"
        exit 1
    }
}

# Push image to registry
function Push-Image {
    if ($Registry -ne "localhost:5000") {
        Write-Info "Pushing image to registry..."

        docker tag "${IMAGE_NAME}:${ImageTag}" "${Registry}/${IMAGE_NAME}:${ImageTag}"
        docker push "${Registry}/${IMAGE_NAME}:${ImageTag}"

        if ($LASTEXITCODE -eq 0) {
            Write-Success "Image pushed to registry successfully"
        }
        else {
            Write-Error "Failed to push image to registry"
            exit 1
        }
    }
    else {
        Write-Info "Skipping image push (using local registry)"
    }
}

# Create namespace
function New-Namespace {
    Write-Info "Creating namespace..."

    kubectl apply -f k8s/namespace.yaml

    if ($LASTEXITCODE -eq 0) {
        Write-Success "Namespace created successfully"
    }
    else {
        Write-Error "Failed to create namespace"
        exit 1
    }
}

# Deploy configuration
function Deploy-Config {
    Write-Info "Deploying secrets and configmaps..."

    kubectl apply -f k8s/secret.yaml
    kubectl apply -f k8s/configmap.yaml

    if ($LASTEXITCODE -eq 0) {
        Write-Success "Secrets and configmaps deployed successfully"
    }
    else {
        Write-Error "Failed to deploy secrets and configmaps"
        exit 1
    }
}

# Deploy storage
function Deploy-Storage {
    Write-Info "Deploying persistent volumes..."

    kubectl apply -f k8s/pvc.yaml

    if ($LASTEXITCODE -eq 0) {
        Write-Success "Persistent volumes deployed successfully"
    }
    else {
        Write-Error "Failed to deploy persistent volumes"
        exit 1
    }
}

# Deploy services
function Deploy-Services {
    Write-Info "Deploying services..."

    kubectl apply -f k8s/service.yaml

    if ($LASTEXITCODE -eq 0) {
        Write-Success "Services deployed successfully"
    }
    else {
        Write-Error "Failed to deploy services"
        exit 1
    }
}

# Deploy application
function Deploy-Application {
    Write-Info "Deploying main application..."

    kubectl apply -f k8s/deployment.yaml

    if ($LASTEXITCODE -eq 0) {
        Write-Success "Application deployed successfully"
    }
    else {
        Write-Error "Failed to deploy application"
        exit 1
    }
}

# Deploy auto-scaling
function Deploy-Autoscaling {
    Write-Info "Deploying auto-scaling configuration..."

    kubectl apply -f k8s/hpa.yaml

    if ($LASTEXITCODE -eq 0) {
        Write-Success "Auto-scaling deployed successfully"
    }
    else {
        Write-Error "Failed to deploy auto-scaling"
        exit 1
    }
}

# Deploy monitoring
function Deploy-Monitoring {
    Write-Info "Deploying monitoring configuration..."

    kubectl apply -f k8s/monitoring.yaml

    if ($LASTEXITCODE -eq 0) {
        Write-Success "Monitoring deployed successfully"
    }
    else {
        Write-Error "Failed to deploy monitoring"
        exit 1
    }
}

# Deploy service mesh
function Deploy-ServiceMesh {
    Write-Info "Deploying service mesh configuration..."

    # Check if Istio is installed
    try {
        kubectl get namespace istio-system | Out-Null
        kubectl apply -f k8s/istio-gateway.yaml

        if ($LASTEXITCODE -eq 0) {
            Write-Success "Service mesh deployed successfully"
        }
        else {
            Write-Error "Failed to deploy service mesh"
            exit 1
        }
    }
    catch {
        Write-Warning "Istio is not installed. Skipping service mesh deployment."
    }
}

# Wait for deployment
function Wait-ForDeployment {
    Write-Info "Waiting for deployment to be ready..."

    kubectl wait --for=condition=available --timeout=300s deployment/swarm-app -n $NAMESPACE

    if ($LASTEXITCODE -eq 0) {
        Write-Success "Deployment is ready"
    }
    else {
        Write-Error "Deployment failed to become ready"
        exit 1
    }
}

# Show status
function Show-Status {
    Write-Info "Deployment status:"

    Write-Host "`n=== Pods ===" -ForegroundColor Cyan
    kubectl get pods -n $NAMESPACE

    Write-Host "`n=== Services ===" -ForegroundColor Cyan
    kubectl get services -n $NAMESPACE

    Write-Host "`n=== Deployments ===" -ForegroundColor Cyan
    kubectl get deployments -n $NAMESPACE

    Write-Host "`n=== HPA ===" -ForegroundColor Cyan
    kubectl get hpa -n $NAMESPACE

    Write-Host "`n=== PVCs ===" -ForegroundColor Cyan
    kubectl get pvc -n $NAMESPACE
}

# Main deployment function
function Deploy {
    Write-Info "Starting V2_SWARM container orchestration deployment..."

    Test-Prerequisites
    Build-Image
    Push-Image
    New-Namespace
    Deploy-Config
    Deploy-Storage
    Deploy-Services
    Deploy-Application
    Deploy-Autoscaling
    Deploy-Monitoring
    Deploy-ServiceMesh
    Wait-ForDeployment
    Show-Status

    Write-Success "V2_SWARM container orchestration deployment completed successfully!"

    Write-Host "`n=== Access Information ===" -ForegroundColor Cyan
    Write-Host "Application: http://swarm.agent-cellphone.local"
    Write-Host "Grafana: http://swarm.agent-cellphone.local/grafana"
    Write-Host "Prometheus: http://swarm.agent-cellphone.local/metrics"

    Write-Host "`n=== Useful Commands ===" -ForegroundColor Cyan
    Write-Host "View logs: kubectl logs -f deployment/swarm-app -n $NAMESPACE"
    Write-Host "Scale deployment: kubectl scale deployment swarm-app --replicas=5 -n $NAMESPACE"
    Write-Host "Port forward: kubectl port-forward service/swarm-app-service 8000:80 -n $NAMESPACE"
}

# Cleanup function
function Remove-Deployment {
    Write-Info "Cleaning up V2_SWARM deployment..."

    kubectl delete namespace $NAMESPACE --ignore-not-found=true

    Write-Success "Cleanup completed"
}

# Help function
function Show-Help {
    Write-Host "V2_SWARM Container Orchestration Deployment Script (PowerShell)" -ForegroundColor Green
    Write-Host ""
    Write-Host "Usage: .\deploy.ps1 [COMMAND] [OPTIONS]"
    Write-Host ""
    Write-Host "Commands:"
    Write-Host "  deploy     Deploy the complete V2_SWARM system"
    Write-Host "  cleanup    Remove the V2_SWARM deployment"
    Write-Host "  status     Show deployment status"
    Write-Host "  help       Show this help message"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Registry  Docker registry URL (default: localhost:5000)"
    Write-Host "  -ImageTag  Docker image tag (default: latest)"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\deploy.ps1 deploy"
    Write-Host "  .\deploy.ps1 deploy -Registry myregistry.com -ImageTag v1.0.0"
    Write-Host "  .\deploy.ps1 cleanup"
    Write-Host "  .\deploy.ps1 status"
    Write-Host ""
}

# Main script logic
switch ($Command) {
    "deploy" {
        Deploy
    }
    "cleanup" {
        Remove-Deployment
    }
    "status" {
        Show-Status
    }
    "help" {
        Show-Help
    }
    default {
        Write-Error "Unknown command: $Command"
        Show-Help
        exit 1
    }
}
