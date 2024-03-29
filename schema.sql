DROP TABLE IF EXISTS `Causality`;
CREATE TABLE IF NOT EXISTS `Causality` 
(
    `texture_mean` FLOAT NOT NULL,
    `area_mean` FLOAT NOT NULL,
    `smoothness_mean` FLOAT NOT NULL,
    `concavity_mean` FLOAT NOT NULL,
    `fractal_dimension_mean` FLOAT NOT NULL,
    `area_se` FLOAT NOT NULL,
    `smoothness_se` FLOAT NOT NULL,
    `concavity_se` FLOAT NOT NULL,
    `fractal_dimension_se` FLOAT NOT NULL,
    `smoothness_worst` FLOAT NOT NULL,
    `concavity_worst` FLOAT NOT NULL,
    `symmetry_worst` FLOAT NOT NULL,
    `fractal_dimension_worst` FLOAT NOT NULL,
    `diagnosis` TEXT NOT NULL,
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;