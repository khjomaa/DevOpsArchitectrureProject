CREATE TABLE IF NOT EXISTS `lines`
(
    `id`              VARCHAR(40)   NOT NULL,
    `object_path`     VARCHAR(250)  NOT NULL,
    `date`            DATETIME(100) NOT NULL,
    `amount_of_lines` INT,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `words`
(
    `id`              INT           NOT NULL AUTO_INCREMENT,
    `object_path`     VARCHAR(250)  NOT NULL,
    `date`            DATETIME(100) NOT NULL,
    `amount_of_words` INT,
    PRIMARY KEY (`id`)
);
