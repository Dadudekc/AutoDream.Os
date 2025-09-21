#!/bin/bash

# V2_SWARM Container Orchestration Deployment Script
# Deploys the complete containerized V2_SWARM system

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
NAMESPACE="swarm-system"
IMAGE_NAME="swarm-agent-cellphone"
IMAGE_TAG="latest"
REGISTRY="localhost:5000"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if kubectl is installed
    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl is not installed. Please install kubectl first."
        exit 1
    fi
    
    # Check if docker is installed
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check if helm is installed (optional)
    if ! command -v helm &> /dev/null; then
        log_warning "Helm is not installed. Some features may not be available."
    fi
    
    # Check kubectl connection
    if ! kubectl cluster-info &> /dev/null; then
        log_error "Cannot connect to Kubernetes cluster. Please check your kubeconfig."
        exit 1
    fi
    
    log_success "Prerequisites check passed"
}

# Build Docker image
build_image() {
    log_info "Building Docker image..."
    
    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
    
    if [ $? -eq 0 ]; then
        log_success "Docker image built successfully"
    else
        log_error "Failed to build Docker image"
        exit 1
    fi
}

# Push image to registry (if registry is specified)
push_image() {
    if [ "$REGISTRY" != "localhost:5000" ]; then
        log_info "Pushing image to registry..."
        
        docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
        docker push ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
        
        if [ $? -eq 0 ]; then
            log_success "Image pushed to registry successfully"
        else
            log_error "Failed to push image to registry"
            exit 1
        fi
    else
        log_info "Skipping image push (using local registry)"
    fi
}

# Create namespace
create_namespace() {
    log_info "Creating namespace..."
    
    kubectl apply -f k8s/namespace.yaml
    
    if [ $? -eq 0 ]; then
        log_success "Namespace created successfully"
    else
        log_error "Failed to create namespace"
        exit 1
    fi
}

# Deploy secrets and configmaps
deploy_config() {
    log_info "Deploying secrets and configmaps..."
    
    kubectl apply -f k8s/secret.yaml
    kubectl apply -f k8s/configmap.yaml
    
    if [ $? -eq 0 ]; then
        log_success "Secrets and configmaps deployed successfully"
    else
        log_error "Failed to deploy secrets and configmaps"
        exit 1
    fi
}

# Deploy persistent volumes
deploy_storage() {
    log_info "Deploying persistent volumes..."
    
    kubectl apply -f k8s/pvc.yaml
    
    if [ $? -eq 0 ]; then
        log_success "Persistent volumes deployed successfully"
    else
        log_error "Failed to deploy persistent volumes"
        exit 1
    fi
}

# Deploy services
deploy_services() {
    log_info "Deploying services..."
    
    kubectl apply -f k8s/service.yaml
    
    if [ $? -eq 0 ]; then
        log_success "Services deployed successfully"
    else
        log_error "Failed to deploy services"
        exit 1
    fi
}

# Deploy main application
deploy_application() {
    log_info "Deploying main application..."
    
    kubectl apply -f k8s/deployment.yaml
    
    if [ $? -eq 0 ]; then
        log_success "Application deployed successfully"
    else
        log_error "Failed to deploy application"
        exit 1
    fi
}

# Deploy auto-scaling
deploy_autoscaling() {
    log_info "Deploying auto-scaling configuration..."
    
    kubectl apply -f k8s/hpa.yaml
    
    if [ $? -eq 0 ]; then
        log_success "Auto-scaling deployed successfully"
    else
        log_error "Failed to deploy auto-scaling"
        exit 1
    fi
}

# Deploy monitoring
deploy_monitoring() {
    log_info "Deploying monitoring configuration..."
    
    kubectl apply -f k8s/monitoring.yaml
    
    if [ $? -eq 0 ]; then
        log_success "Monitoring deployed successfully"
    else
        log_error "Failed to deploy monitoring"
        exit 1
    fi
}

# Deploy service mesh (Istio)
deploy_service_mesh() {
    log_info "Deploying service mesh configuration..."
    
    # Check if Istio is installed
    if kubectl get namespace istio-system &> /dev/null; then
        kubectl apply -f k8s/istio-gateway.yaml
        
        if [ $? -eq 0 ]; then
            log_success "Service mesh deployed successfully"
        else
            log_error "Failed to deploy service mesh"
            exit 1
        fi
    else
        log_warning "Istio is not installed. Skipping service mesh deployment."
    fi
}

# Wait for deployment to be ready
wait_for_deployment() {
    log_info "Waiting for deployment to be ready..."
    
    kubectl wait --for=condition=available --timeout=300s deployment/swarm-app -n ${NAMESPACE}
    
    if [ $? -eq 0 ]; then
        log_success "Deployment is ready"
    else
        log_error "Deployment failed to become ready"
        exit 1
    fi
}

# Show deployment status
show_status() {
    log_info "Deployment status:"
    
    echo ""
    echo "=== Pods ==="
    kubectl get pods -n ${NAMESPACE}
    
    echo ""
    echo "=== Services ==="
    kubectl get services -n ${NAMESPACE}
    
    echo ""
    echo "=== Deployments ==="
    kubectl get deployments -n ${NAMESPACE}
    
    echo ""
    echo "=== HPA ==="
    kubectl get hpa -n ${NAMESPACE}
    
    echo ""
    echo "=== PVCs ==="
    kubectl get pvc -n ${NAMESPACE}
}

# Main deployment function
deploy() {
    log_info "Starting V2_SWARM container orchestration deployment..."
    
    check_prerequisites
    build_image
    push_image
    create_namespace
    deploy_config
    deploy_storage
    deploy_services
    deploy_application
    deploy_autoscaling
    deploy_monitoring
    deploy_service_mesh
    wait_for_deployment
    show_status
    
    log_success "V2_SWARM container orchestration deployment completed successfully!"
    
    echo ""
    echo "=== Access Information ==="
    echo "Application: http://swarm.agent-cellphone.local"
    echo "Grafana: http://swarm.agent-cellphone.local/grafana"
    echo "Prometheus: http://swarm.agent-cellphone.local/metrics"
    echo ""
    echo "=== Useful Commands ==="
    echo "View logs: kubectl logs -f deployment/swarm-app -n ${NAMESPACE}"
    echo "Scale deployment: kubectl scale deployment swarm-app --replicas=5 -n ${NAMESPACE}"
    echo "Port forward: kubectl port-forward service/swarm-app-service 8000:80 -n ${NAMESPACE}"
}

# Cleanup function
cleanup() {
    log_info "Cleaning up V2_SWARM deployment..."
    
    kubectl delete namespace ${NAMESPACE} --ignore-not-found=true
    
    log_success "Cleanup completed"
}

# Help function
show_help() {
    echo "V2_SWARM Container Orchestration Deployment Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  deploy     Deploy the complete V2_SWARM system"
    echo "  cleanup    Remove the V2_SWARM deployment"
    echo "  status     Show deployment status"
    echo "  help       Show this help message"
    echo ""
    echo "Environment Variables:"
    echo "  REGISTRY   Docker registry URL (default: localhost:5000)"
    echo "  IMAGE_TAG  Docker image tag (default: latest)"
    echo ""
}

# Main script logic
case "${1:-deploy}" in
    deploy)
        deploy
        ;;
    cleanup)
        cleanup
        ;;
    status)
        show_status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        log_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
