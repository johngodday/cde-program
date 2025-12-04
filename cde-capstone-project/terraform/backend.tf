terraform {
  required_version = ">= 1.5.0"
  backend "s3" {
    bucket = "capstone-terra-state"
    key    = "data-platform/terraform.tfstate"
    region = "us-west-2"
  }
}
