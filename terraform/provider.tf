provider "aws" {
  region = var.region # Default set in variables.tf
}

terraform {
  backend "s3" {
    bucket         = "my-tf-state-bucket" # Update this
    region         = "eu-west-2"          # Update this
    encrypt        = true
  }
}