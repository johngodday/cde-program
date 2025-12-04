
resource "aws_s3_bucket" "destination" {
  bucket = var.destination_bucket_name

  versioning {
    enabled = true
  }

  tags = {
    Name = var.destination_bucket_name
    Env  = "dev"
    Team = "data-platform"
  }
}