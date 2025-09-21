resource "aws_db_instance" "dream-os_rds" {
  identifier     = "dream-os-rds"
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = "db.t3.micro"
  allocated_storage = 20
  storage_encrypted = true
  
  db_name  = "dreamos"
  username = "admin"
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  tags = {
    Name        = "dream-os-rds"
    Environment = "production"
  }
}
