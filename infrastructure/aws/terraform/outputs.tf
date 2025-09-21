# V3-001: Cloud Infrastructure Setup - AWS Outputs
# Agent-1: Architecture Foundation Specialist

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.swarm_vpc.id
}

output "vpc_cidr_block" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.swarm_vpc.cidr_block
}

output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value       = aws_subnet.public_subnets[*].id
}

output "private_subnet_ids" {
  description = "IDs of the private subnets"
  value       = aws_subnet.private_subnets[*].id
}

output "eks_cluster_id" {
  description = "ID of the EKS cluster"
  value       = aws_eks_cluster.swarm_cluster.id
}

output "eks_cluster_arn" {
  description = "ARN of the EKS cluster"
  value       = aws_eks_cluster.swarm_cluster.arn
}

output "eks_cluster_endpoint" {
  description = "Endpoint for EKS cluster"
  value       = aws_eks_cluster.swarm_cluster.endpoint
}

output "eks_cluster_security_group_id" {
  description = "Security group ID attached to the EKS cluster"
  value       = aws_eks_cluster.swarm_cluster.vpc_config[0].cluster_security_group_id
}

output "eks_node_group_arn" {
  description = "ARN of the EKS node group"
  value       = aws_eks_node_group.swarm_nodes.arn
}

output "rds_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.swarm_database.endpoint
}

output "rds_port" {
  description = "RDS instance port"
  value       = aws_db_instance.swarm_database.port
}

output "redis_endpoint" {
  description = "Redis cluster endpoint"
  value       = aws_elasticache_replication_group.swarm_redis.primary_endpoint_address
}

output "redis_port" {
  description = "Redis cluster port"
  value       = aws_elasticache_replication_group.swarm_redis.port
}

output "kms_key_id" {
  description = "KMS key ID for encryption"
  value       = aws_kms_key.swarm_kms_key.key_id
}

output "kms_key_arn" {
  description = "KMS key ARN for encryption"
  value       = aws_kms_key.swarm_kms_key.arn
}



