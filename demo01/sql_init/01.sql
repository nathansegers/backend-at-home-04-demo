-- Using database `users`
-- Table structure for table `users`
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name` varchar(255) NULL,
  `age` tinyint NOT NULL,
  `biography` text NOT NULL,
  `registrationDate` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP
);

-- Table structure for table `books`
CREATE TABLE `books` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `title` varchar(255) NULL,
  `author` varchar(255) NULL,
  `year` int NOT NULL,
  `publisher` varchar(255) NULL,
  `description` longtext NOT NULL
);


