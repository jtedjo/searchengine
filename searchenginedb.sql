CREATE TABLE `tokens` (
  `word` varchar(2048) NOT NULL,
  `term_frequency` int(11) DEFAULT NULL,
  `doc_id` VARCHAR(50) NOT NULL,
  `file_name` varchar(2048) NOT NULL,
  `tfandidf` int(11) DEFAULT NULL,
  PRIMARY KEY (`word`,`doc_id`)
);


CREATE TABLE `idf` (
  `word` varchar(250) NOT NULL,
  `counts` decimal(6,2) DEFAULT NULL,
  PRIMARY KEY (`word`),
  CONSTRAINT `idf_ibfk_1` FOREIGN KEY (`word`) REFERENCES `tokens` (`word`)
);

