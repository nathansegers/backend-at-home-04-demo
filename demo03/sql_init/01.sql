-- Using database `authors`
-- Table structure for table `authors`
CREATE TABLE `authors` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name` varchar(255) NULL,
  `gender` varchar(20) NOT NULL,
  `birthdate` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP
);

-- Table structure for table `books`
CREATE TABLE `books` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `title` varchar(255) NULL,
  `author_id` int NULL,
  `year` int NOT NULL,
  `publisher` varchar(255) NULL,
  `description` longtext NOT NULL,
  FOREIGN KEY (author_id) REFERENCES authors(id)
);


