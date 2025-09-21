resource "aws_elasticache_replication_group" "dream-os_redis" {
  replication_group_id = "dream-os-redis"
  description          = "Redis cluster for Dream.OS"
  
  node_type            = "cache.t3.micro"
  port                 = 6379
  parameter_group_name = "default.redis7"
  num_cache_clusters   = 2
  
  subnet_group_name = aws_elasticache_subnet_group.main.name
  security_group_ids = [aws_security_group.redis.id]
  
  tags = {
    Name        = "dream-os-redis"
    Environment = "production"
  }
}
