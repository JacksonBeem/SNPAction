provider "aws" { region = var.aws_region }

resource "random_id" "suffix" { byte_length = 4 }

locals {
  bucket_name = lower("${var.project_name}-${random_id.suffix.hex}")
}


