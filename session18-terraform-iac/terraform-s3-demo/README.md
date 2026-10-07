# Terraform S3 Demo

Copy `terraform.tfvars.example` to `terraform.tfvars` and set a globally unique name. Configure AWS first with `aws configure` (never commit credentials).

```powershell
terraform init
terraform fmt -check
terraform validate
terraform plan
terraform apply
terraform show
terraform output
terraform destroy
```

The configuration creates an encrypted, versioned, private S3 bucket. `plan` is safe and previews changes; `apply` creates billable AWS resources; always run `destroy` when the lab is complete.

## Verification status

Terraform and the AWS CLI are installed locally; `terraform fmt` has been run on this configuration. `init`, `plan`, `apply`, `show`, `output`, and `destroy` are intentionally pending AWS credentials and a chosen globally unique bucket name. Run them only after `aws configure` is completed.

## Local no-account option

This repository includes LocalStack support. It emulates S3 locally—no AWS account, credentials, or billing required.

```powershell
docker compose -f ../../localstack-compose.yml up -d
terraform init
terraform plan -var-file=local.tfvars
terraform apply -auto-approve -var-file=local.tfvars
terraform show
terraform output
terraform destroy -auto-approve -var-file=local.tfvars
```

Use local evidence for learning; it is not proof of resources created in a real AWS account.
