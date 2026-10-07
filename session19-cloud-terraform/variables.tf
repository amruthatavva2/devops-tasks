variable "aws_region" {
  type    = string
  default = "ap-south-1"
}
variable "project" {
  type    = string
  default = "devops-cloud-lab"
}
variable "vpc_cidr" {
  type    = string
  default = "10.20.0.0/16"
}
variable "public_subnet_cidr" {
  type    = string
  default = "10.20.1.0/24"
}
variable "key_name" {
  type        = string
  description = "Existing EC2 key pair name"
}
variable "bucket_name" {
  type        = string
  description = "Globally unique S3 bucket name"
}
variable "ami_id" {
  type        = string
  description = "Amazon Linux AMI ID for selected region"
}
variable "local_mode" {
  type    = bool
  default = false
}
variable "localstack_endpoint" {
  type    = string
  default = "http://localhost:4566"
}
