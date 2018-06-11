BEGIN TRANSACTION;
CREATE TABLE "simulations" (
	`simulationId`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`forgetTime`	INTEGER
);
CREATE TABLE `sent` (
	`nodeId`	INTEGER,
	`informationId`	INTEGER,
	FOREIGN KEY(`nodeId`) REFERENCES nodes(nodeId),
	FOREIGN KEY(`informationId`) REFERENCES informations(informationId)
);
CREATE TABLE `received` (
	`nodeId`	INTEGER,
	`informationId`	INTEGER,
	FOREIGN KEY(`nodeId`) REFERENCES nodes(nodeId),
	FOREIGN KEY(`informationId`) REFERENCES informations(informationId)
);
CREATE TABLE "nodes" (
	`nodeId`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`internalId`	INTEGER,
	`pConnect`	REAL,
	`pSend`	REAL,
	`pLike`	REAL,
	`pConsult`	REAL,
	`networkId`	INTEGER,
	FOREIGN KEY(`networkId`) REFERENCES networks ( networkId )
);
CREATE TABLE "networks" (
	`networkId`	INTEGER,
	`size`	INTEGER,
	`simulationId`	INTEGER,
	PRIMARY KEY(networkId),
	FOREIGN KEY(`simulationId`) REFERENCES simulations(simulationId)
);
CREATE TABLE `liked` (
	`nodeId`	INTEGER,
	`informationId`	INTEGER,
	FOREIGN KEY(`nodeId`) REFERENCES nodes(nodeId),
	FOREIGN KEY(`informationId`) REFERENCES informations(informationId)
);
CREATE TABLE "informations" (
	`informationId`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`internalId`	INTEGER,
	`networkId`	INTEGER,
	`dead`	INTEGER,
	FOREIGN KEY(`networkId`) REFERENCES networks ( networkId )
);
CREATE TABLE `consulted` (
	`nodeId`	INTEGER,
	`informationId`	INTEGER,
	FOREIGN KEY(`nodeId`) REFERENCES nodes(nodeId),
	FOREIGN KEY(`informationId`) REFERENCES informations(informationId)
);
CREATE TABLE `consultables` (
	`informationId`	INTEGER,
	`nodeId`	INTEGER,
	`value`	TEXT,
	FOREIGN KEY(`informationId`) REFERENCES informations(informationId),
	FOREIGN KEY(`nodeId`) REFERENCES nodes(nodeId)
);
CREATE TABLE "connections" (
	`networkId`	INTEGER,
	`startNode`	INTEGER,
	`endNode`	INTEGER,
	FOREIGN KEY(`networkId`) REFERENCES networks ( networkId ),
	FOREIGN KEY(`startNode`) REFERENCES nodes ( nodeId ),
	FOREIGN KEY(`endNode`) REFERENCES nodes ( nodeId )
);
COMMIT;
