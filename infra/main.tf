#RECURSO

resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

#LO TOMAMOS DE CARPETA MODULES/STORAGE
module "storage" {
  source          = "./modules/storage"
  name            = var.storage_account_name
  resource_group  = azurerm_resource_group.rg.name
  location        = var.location
}


#LO TOMAMOS DE CARPETA MODULES/ADF

module "adf" {
  source         = "./modules/adf"
  name           = "adf-finbankdata"
  location       = var.location
  resource_group = azurerm_resource_group.rg.name
}

#KEY VAULT, LO TOMAMOS DE CARPETA MODULES/KEYVAULT
module "keyvault" {
  source         = "./modules/keyvault"
  name           = "kv-finbankdata"
  location       = var.location
  resource_group = azurerm_resource_group.rg.name
  tenant_id      = var.tenant_id

  sql_admin_password = var.sql_admin_password
}


#SQL LO TOMAMOS DE CARPETA MODULES/SQL

module "sql" {
  source          = "./modules/sql"
  server_name     = "sql-finbankdata"
  db_name         = "sqldb-finbankdata"
  resource_group  = azurerm_resource_group.rg.name
  location        = azurerm_resource_group.rg.location
  admin_user      = "sqladminuser"
  admin_password  = var.sql_admin_password

}

#DATABRICKS LO TOMAMOS DE CARPETA MODULES/DATABRICKS
module "databricks" {
  source              = "./modules/databricks"
  databricks_name     = "adb-finbankdata"
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.location
}
