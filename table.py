from azure.cosmosdb.table import TableService

conn_string = "DefaultEndpointsProtocol=https;AccountName=hackgt19;AccountKey=VluI82NNObOQHE95tf8333Mdkg5lKMS5ejHT6vHeITXlIrjIcPNAzENYTFI4qRNK1OaltlIx4qHozbCdpallqQ==;TableEndpoint=https://hackgt19.table.cosmos.azure.com:443/;"
# table = TableService(endpoint_suffix = "table.cosmos.azure.com", connection_string= the_connection_string)
table = TableService(connection_string=conn_string)

print(table)

table.create_table("test")
print(table.get_table("test"))