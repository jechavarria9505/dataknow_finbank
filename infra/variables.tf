variable "location" {
  default = "centralus"
}

variable "resource_group_name" {
  default = "rg-finbank-dataknow"
}

variable "storage_account_name" {
  default = "stfinbankdata"
}


variable "tenant_id" {
  description = "Azure Tenant ID"
  type        = string
}

variable "sql_admin_password" {
  sensitive = true
}