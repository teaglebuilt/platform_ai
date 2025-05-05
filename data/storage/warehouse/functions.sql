CREATE OR REPLACE EXTERNAL FUNCTION PII_tokenize_str (value varchar)
  RETURNS varchar STABLE
  LAMBDA 'your_lambda_function_name'
  IAM_ROLE 'your_redshift_role_arn';

CREATE OR REPLACE EXTERNAL FUNCTION PII_tokenize_int (value int)
  RETURNS varchar STABLE
  LAMBDA 'your_lambda_function_name'
  IAM_ROLE 'your_redshift_role_arn';
