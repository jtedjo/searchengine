CREATE TABLE `tokens` (
  `word` varchar(2048) NOT NULL,
  `term_frequency` decimal(6,2) DEFAULT NULL,
  `doc_id` VARCHAR(50) NOT NULL,
  `tfandidf` decimal(6,2) DEFAULT NULL,
  PRIMARY KEY (`word`,`doc_id`)
);


CREATE TABLE `idf` (
  `word` varchar(250) NOT NULL,
  `counts` decimal(6,2) DEFAULT NULL,
  PRIMARY KEY (`word`),
  CONSTRAINT `idf_ibfk_1` FOREIGN KEY (`word`) REFERENCES `tokens` (`word`)
);

