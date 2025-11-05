resource "aws_s3_bucket" "cde-user-oluwakayode" {
  bucket = "cde-user-oluwakayode"

  tags = {
    Name        = "Data Engineer"
    Environment = "Dev"
  }
}

resource "aws_glue_catalog_database" "cde-oluwakayode-db" {
  name = "cdeoluwakayodedb"
}
