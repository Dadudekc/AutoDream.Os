resource "aws_eks_cluster" "dream-os_eks" {
  name     = "dream-os-eks"
  role_arn = aws_iam_role.eks_cluster_role.arn
  version  = "1.28"

  vpc_config {
    subnet_ids              = [aws_subnet.private_1.id, aws_subnet.private_2.id]
    endpoint_private_access = true
    endpoint_public_access  = true
  }

  tags = {
    Name        = "dream-os-eks"
    Environment = "production"
  }
}
