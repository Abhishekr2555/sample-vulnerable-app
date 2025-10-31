# NOTE: contains intentional security test patterns for SAST/SCA/IaC scanning.
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "app_bucket" {
  bucket = "sample-app-terraform-bucket-12345"
  acl    = "private"  # Fixed: Changed from "public-read" to "private" for better security
}

resource "aws_iam_policy" "app_policy" {
  name        = "app-restricted-access"  # Changed: Updated policy name to reflect restricted access
  description = "Policy used by instances with restricted permissions"  # Updated description

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]  # Fixed: Replaced wildcard "*" with specific required actions
        Resource = [
          "arn:aws:s3:::sample-app-terraform-bucket-12345",
          "arn:aws:s3:::sample-app-terraform-bucket-12345/*"
        ]  # Fixed: Replaced wildcard "*" with specific bucket ARN
      }
    ]
  })
}

resource "aws_security_group" "restricted_sg" {  # Changed: Renamed to reflect restricted access
  name        = "restricted-sg"
  description = "Security group with restricted access"  # Updated description

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]  # Fixed: Restricted to internal network range
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]  # Fixed: Restricted to internal network range
  }
}