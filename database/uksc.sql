-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 08, 2025 at 02:03 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `uksc`
--

-- --------------------------------------------------------

--
-- Table structure for table `uksc_academy`
--

CREATE TABLE `uksc_academy` (
  `sno` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `email` varchar(200) NOT NULL,
  `phno` varchar(20) NOT NULL,
  `crs` varchar(20) NOT NULL,
  `age` varchar(3) NOT NULL,
  `address` varchar(5000) NOT NULL,
  `date` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `uksc_academy`
--

INSERT INTO `uksc_academy` (`sno`, `name`, `email`, `phno`, `crs`, `age`, `address`, `date`) VALUES
(1, 'Sample', 'Sample@gmail.com', '9191919191', '', '22', 'Sample', '2025-03-08'),
(13, 'Supravo Sarkar', 'thefootballlab21@gmail.com', '09002734342', 'PL0000434100', '22', 'DD-18/7, Salt Lake Sector-3, Kolkata', '2025-03-09'),
(14, 'Supravo Sarkar', 'supravosarkar41@gmail.com', '09002734342', 'PL0000434100', '22', 'DD-18/7, Salt Lake Sector-3, Kolkata', '2025-03-11');

-- --------------------------------------------------------

--
-- Table structure for table `uksc_contact`
--

CREATE TABLE `uksc_contact` (
  `sno1` int(11) NOT NULL,
  `name1` varchar(200) NOT NULL,
  `email1` varchar(200) NOT NULL,
  `phno1` varchar(20) NOT NULL,
  `msg` text NOT NULL,
  `date` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `uksc_contact`
--

INSERT INTO `uksc_contact` (`sno1`, `name1`, `email1`, `phno1`, `msg`, `date`) VALUES
(1, 'Sample', 'Sample@gmail.com', '9899989898', 'Sample Message', '2025-03-09');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `uksc_academy`
--
ALTER TABLE `uksc_academy`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `uksc_contact`
--
ALTER TABLE `uksc_contact`
  ADD PRIMARY KEY (`sno1`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `uksc_academy`
--
ALTER TABLE `uksc_academy`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `uksc_contact`
--
ALTER TABLE `uksc_contact`
  MODIFY `sno1` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
