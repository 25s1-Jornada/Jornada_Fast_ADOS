// NOTE: The following script syntax is valid for database version 5.0 and above.

:param {
  // Define the file path root and the individual file names required for loading.
  // https://neo4j.com/docs/operations-manual/current/configuration/file-locations/
  file_path_root: 'file:///', // Change this to the folder your script can access the files at.
  file_0: 'Dados-Tabela-Cliente.csv',
  file_1: 'Dados-Tabela-OS.csv'
};

// CONSTRAINT creation
// -------------------
//
// Create node uniqueness constraints, ensuring no duplicates for the given node label and ID property exist in the database. This also ensures no duplicates are introduced in future.
//
CREATE CONSTRAINT `Dados-Tabela-Cliente.csv` IF NOT EXISTS
FOR (n: `Client`)
REQUIRE (n.`clientId`) IS UNIQUE;
CREATE CONSTRAINT `Dados-Tabela-OS.csv` IF NOT EXISTS
FOR (n: `ServiceOrder`)
REQUIRE (n.`osId`) IS UNIQUE;

:param {
  idsToSkip: []
};

// NODE load
// ---------
//
// Load nodes in batches, one node label at a time. Nodes will be created using a MERGE statement to ensure a node with the same label and ID property remains unique. Pre-existing nodes found by a MERGE statement will have their other properties set to the latest values encountered in a load file.
//
// NOTE: Any nodes with IDs in the 'idsToSkip' list parameter will not be loaded.
LOAD CSV WITH HEADERS FROM ($file_path_root + $file_0) AS row
WITH row
WHERE NOT row.`clientId` IN $idsToSkip AND NOT toInteger(trim(row.`clientId`)) IS NULL
CALL (row) {
  MERGE (n: `Client` { `clientId`: toInteger(trim(row.`clientId`)) })
  SET n.`clientId` = toInteger(trim(row.`clientId`))
  SET n.`clientName` = row.`Nome Cliente`
  SET n.`city` = row.`Cidade`
  SET n.`state` = row.`Estado`
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_1) AS row
WITH row
WHERE NOT row.`osId` IN $idsToSkip AND NOT toInteger(trim(row.`osId`)) IS NULL
CALL (row) {
  MERGE (n: `ServiceOrder` { `osId`: toInteger(trim(row.`osId`)) })
  SET n.`osId` = toInteger(trim(row.`osId`))
  SET n.`date` = row.`data`
  SET n.`ticketNumber` = toInteger(trim(row.`Nr.Chamado`))
  SET n.`clientName` = row.`Nome Cliente`
  SET n.`city` = row.`Cidade`
  SET n.`state` = row.`Estado`
  SET n.`serialNumber` = toInteger(trim(row.`Nr.Serie`))
  SET n.`item` = row.`Item`
  SET n.`manufacturingDate` = row.`Dt.Fabricacao`
  SET n.`invoiceIssueDate` = row.`Dt.Emissao NF`
  SET n.`type` = row.`Tipo`
  SET n.`cause` = row.`Causa`
  SET n.`observation` = row.`Observacao`
} IN TRANSACTIONS OF 10000 ROWS;


// RELATIONSHIP load
// -----------------
//
// Load relationships in batches, one relationship type at a time. Relationships are created using a MERGE statement, meaning only one relationship of a given type will ever be created between a pair of nodes.
LOAD CSV WITH HEADERS FROM ($file_path_root + $file_1) AS row
WITH row 
CALL (row) {
  MATCH (source: `ServiceOrder` { `osId`: toInteger(trim(row.`osId`)) })
  MATCH (target: `Client` { `clientId`: toInteger(trim(row.`Cod.Cliente`)) })
  MERGE (source)-[r: `BELONGS_TO`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;
