variable "aws_region" {
  type    = string
  default = "us-west-2"
}

variable "destination_bucket_name" {
  description = "S3 bucket in your account to write processed data"
  type        = string
  default     = "capstone-dumps"
}


variable "source_bucket_arn" {
  description = "ARN of the source bucket (external account)"
  type        = string
  default     = "arn:aws:s3:::core-telecoms-data-lake"
}

variable "source_bucket_name" {
  description = "Name of source bucket (used for ListBucket permission)"
  type        = string
  default     = "core-telecoms-data-lake"
}
