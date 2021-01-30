DROP TABLE IF EXISTS exchange_history;

CREATE TABLE exchange_history
(
`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
`currency_to` VARCHAR(5) NOT NULL,
`exchange_rate` FLOAT(10,2) NOT NULL,
`amount` FLOAT(10,2) NOT NULL,
`result` DOUBLE(10,2) NOT NULL
);