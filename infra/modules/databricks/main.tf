resource "azurerm_databricks_workspace" "databricks" {
  name                = var.databricks_name
  resource_group_name = var.resource_group_name
  location            = var.location

  sku = "premium"

  managed_resource_group_name = "${var.databricks_name}-managed-rg"

  public_network_access_enabled = true

  tags = {
    environment = "dev"
    project     = "data-engineer-test"
  }
}