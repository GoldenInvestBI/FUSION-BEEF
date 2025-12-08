CREATE TABLE `products` (
	`id` int AUTO_INCREMENT NOT NULL,
	`sku` varchar(50) NOT NULL,
	`name` varchar(500) NOT NULL,
	`category` varchar(100) NOT NULL,
	`priceOriginal` varchar(20) NOT NULL,
	`priceWithMarkup` varchar(20) NOT NULL,
	`markup` varchar(10) NOT NULL DEFAULT '60.00',
	`imageUrl` text,
	`imageLocalPath` text,
	`description` text,
	`inStock` int NOT NULL DEFAULT 1,
	`stockStatus` varchar(50),
	`weight` varchar(50),
	`origin` varchar(100),
	`brand` varchar(100),
	`minervaUrl` text,
	`lastScrapedAt` timestamp,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	`updatedAt` timestamp NOT NULL DEFAULT (now()) ON UPDATE CURRENT_TIMESTAMP,
	CONSTRAINT `products_id` PRIMARY KEY(`id`),
	CONSTRAINT `products_sku_unique` UNIQUE(`sku`)
);
--> statement-breakpoint
CREATE TABLE `scrape_logs` (
	`id` int AUTO_INCREMENT NOT NULL,
	`status` varchar(50) NOT NULL,
	`productsFound` int DEFAULT 0,
	`productsAdded` int DEFAULT 0,
	`productsUpdated` int DEFAULT 0,
	`productsRemoved` int DEFAULT 0,
	`errorMessage` text,
	`details` text,
	`startedAt` timestamp NOT NULL,
	`completedAt` timestamp,
	`duration` int,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	CONSTRAINT `scrape_logs_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE TABLE `settings` (
	`id` int AUTO_INCREMENT NOT NULL,
	`key` varchar(100) NOT NULL,
	`value` text NOT NULL,
	`description` text,
	`updatedAt` timestamp NOT NULL DEFAULT (now()) ON UPDATE CURRENT_TIMESTAMP,
	CONSTRAINT `settings_id` PRIMARY KEY(`id`),
	CONSTRAINT `settings_key_unique` UNIQUE(`key`)
);
