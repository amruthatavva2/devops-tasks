variable "aws_region" {
  type    = string
  default = "ap-south-1"
}
variable "bucket_name" {
  type        = string
  description = "Globally unique S3 bucket name"
}
variable "environment" {
  type    = string
  default = "dev"
}
variable "local_mode" { type = bool; default = false }
variable "localstack_endpoint" { type = string; default = "http://localhost:4566" }
