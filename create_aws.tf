provider "aws" {
  region                      = "us-east-1"
  access_key                  = "fake"
  secret_key                  = "fake"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    lambda   = "http://0.0.0.0:4566"
    kinesis  = "http://0.0.0.0:4566"
  }
}



// KINESIS STREAMS
resource "aws_kinesis_stream" "get_records_stream" {
  name = "my-stream"
  shard_count = 1
  retention_period = 24

  shard_level_metrics = [
    "IncomingBytes",
    "OutgoingBytes",
  ]
}



// LAMBDA FUNCTIONS
resource "aws_lambda_function" "processor_lambda" {
 function_name = "my-lambda"
  filename      = "lambda_zip.zip"
  handler       = "lambda_function.lambda_handler"
  role          = "arn:aws:iam::000000000000:role/lambda-role"
  runtime       = "python3.7"
  timeout       = 10
  memory_size   = 128
}



// LAMBDA TRIGGERS
resource "aws_lambda_event_source_mapping" "lambda_processor_trigger" {
  event_source_arn              = "arn:aws:kinesis:us-east-1:000000000000:stream/mystream"
  function_name                 = "my-lambda"
  batch_size                    = 100
  starting_position             = "LATEST"
  enabled                       = true
  maximum_record_age_in_seconds = 604800
}
