-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 15, 2026 at 06:18 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `srmss_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `schedule_id` int(11) NOT NULL,
  `booking_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `travel_date` date NOT NULL,
  `passenger_count` int(11) DEFAULT 1,
  `total_fare` decimal(10,2) DEFAULT 0.00,
  `status` varchar(20) DEFAULT 'confirmed',
  `seat_numbers` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bookings`
--

INSERT INTO `bookings` (`id`, `customer_id`, `schedule_id`, `booking_date`, `travel_date`, `passenger_count`, `total_fare`, `status`, `seat_numbers`) VALUES
(1, 7, 7, '2026-06-04 02:22:36', '2026-06-04', 2, 0.00, 'cancelled', NULL),
(2, 7, 7, '2026-06-04 02:24:54', '2026-06-04', 3, 0.00, 'confirmed', NULL),
(5, 1, 15, '2026-06-08 14:00:35', '2026-06-09', 1, 350.00, 'cancelled', NULL),
(6, 1, 15, '2026-06-11 16:58:52', '2026-06-12', 3, 1650.00, 'confirmed', NULL),
(7, 7, 11, '2026-06-11 17:25:10', '2026-06-11', 1, 0.00, 'confirmed', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `driver_locations`
--

CREATE TABLE `driver_locations` (
  `id` int(11) NOT NULL,
  `driver_id` int(11) NOT NULL,
  `schedule_id` int(11) DEFAULT NULL,
  `latitude` decimal(10,8) NOT NULL,
  `longitude` decimal(11,8) NOT NULL,
  `speed` decimal(5,2) DEFAULT 0.00,
  `heading` varchar(10) DEFAULT 'N',
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `driver_locations`
--

INSERT INTO `driver_locations` (`id`, `driver_id`, `schedule_id`, `latitude`, `longitude`, `speed`, `heading`, `updated_at`, `created_at`) VALUES
(1, 6, 7, 9.66150000, 80.02550000, 80.00, 'NE', '2026-06-04 17:33:25', '2026-06-03 09:53:04'),
(2, 8, NULL, 5.94925100, 80.54388400, 0.00, 'N', '2026-06-04 15:06:06', '2026-06-03 17:49:51'),
(3, 6, 7, 9.66150000, 80.02550000, 80.00, 'NE', '2026-06-04 17:33:25', '2026-06-04 08:43:03'),
(4, 6, 7, 9.66150000, 80.02550000, 80.00, 'NE', '2026-06-04 17:33:25', '2026-06-04 09:22:25'),
(5, 6, NULL, 7.02939184, 79.95423381, 62.00, 'NE', '2026-06-04 10:28:59', '2026-06-04 09:40:35'),
(6, 6, NULL, 5.94925100, 80.54388400, 0.00, 'N', '2026-06-04 14:53:16', '2026-06-04 09:40:35'),
(8, 6, NULL, 7.02939184, 79.95423381, 62.00, 'NE', '2026-06-04 10:28:59', '2026-06-04 10:15:11'),
(9, 24, 11, 5.94925100, 80.54388400, 0.00, 'N', '2026-06-06 13:20:08', '2026-06-06 13:19:00'),
(10, 24, 11, 5.94925100, 80.54388400, 0.00, 'N', '2026-06-06 13:20:08', '2026-06-06 13:19:00'),
(11, 6, NULL, 5.94922820, 80.54392190, 0.00, 'N', '2026-06-12 08:15:25', '2026-06-12 07:56:39'),
(12, 6, NULL, 5.94922820, 80.54392190, 0.00, 'N', '2026-06-12 08:15:25', '2026-06-12 07:56:39'),
(13, 1, NULL, 5.94921471, 80.54405633, 0.00, 'N', '2026-06-12 07:59:21', '2026-06-12 07:57:19');

-- --------------------------------------------------------

--
-- Table structure for table `fuel_logs`
--

CREATE TABLE `fuel_logs` (
  `id` int(11) NOT NULL,
  `vehicle_id` int(11) NOT NULL,
  `fuel_date` date NOT NULL,
  `fuel_liters` decimal(10,2) NOT NULL,
  `cost_per_liter` decimal(10,2) NOT NULL,
  `total_cost` decimal(12,2) NOT NULL,
  `odometer_reading` int(11) NOT NULL,
  `fuel_station` varchar(200) DEFAULT NULL,
  `receipt_path` varchar(500) DEFAULT NULL,
  `logged_by` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `fuel_logs`
--

INSERT INTO `fuel_logs` (`id`, `vehicle_id`, `fuel_date`, `fuel_liters`, `cost_per_liter`, `total_cost`, `odometer_reading`, `fuel_station`, `receipt_path`, `logged_by`, `created_at`) VALUES
(1, 1, '2026-06-04', 85.00, 330.00, 28050.00, 125550, 'Ceypetco', NULL, NULL, '2026-06-03 08:54:27'),
(2, 1, '2026-06-03', 10.00, 220.00, 2200.00, 1000, 'Ceypetco', NULL, 6, '2026-06-03 17:47:22'),
(3, 1, '2026-06-03', 75.00, 220.00, 16500.00, 41, 'Ceypetco', 'uploads/receipts/fuel_6_20260604_081036_correct.pdf', 6, '2026-06-04 02:40:37'),
(4, 1, '2026-06-04', 41.00, 330.00, 13530.00, 147, 'Ceypetco', 'uploads/receipts/fuel_6_20260604_111022_correct.pdf', 6, '2026-06-04 05:40:22'),
(5, 4, '2026-06-04', 45.00, 330.00, 14850.00, 14, 'Ceypetco', 'uploads/receipts/fuel_6_20260604_114316.pdf', 6, '2026-06-04 06:13:16'),
(6, 4, '2026-06-04', 10.00, 10.00, 100.00, 10, 'Ceypetco', 'uploads/receipts/fuel_6_20260604_120940.pdf', 6, '2026-06-04 06:39:40'),
(7, 4, '2026-06-04', 11.00, 11.00, 121.00, 11, 'Ceypetco', 'uploads/receipts/fuel_6_20260604_121243.pdf', 6, '2026-06-04 06:42:43'),
(8, 4, '2026-06-04', 45.00, 45.00, 2025.00, 45, 'Ceypetco', 'uploads/receipts/fuel_6_20260604_121343.jpg', 6, '2026-06-04 06:43:43'),
(9, 2, '2026-06-04', 4.00, 330.00, 1320.00, 10, 'Ceypetco', NULL, 1, '2026-06-05 07:36:07'),
(10, 5, '2026-06-06', 12.00, 330.00, 3960.00, 44, 'Ceypetco', 'uploads/receipts/fuel_24_20260606_185046.pdf', 24, '2026-06-06 13:20:46'),
(12, 1, '2026-06-05', 75.00, 320.00, 24000.00, 42000, 'Lanka IOC', NULL, 1, '2026-06-08 13:40:16'),
(13, 4, '2026-06-08', 90.00, 330.00, 29700.00, 25000, 'Ceypetco', NULL, 1, '2026-06-08 13:40:16'),
(14, 6, '2026-06-08', 15.00, 330.00, 4950.00, 1150, 'Matara', 'uploads/receipts/fuel_1_20260609_002020.pdf', 1, '2026-06-08 18:50:20');

-- --------------------------------------------------------

--
-- Table structure for table `maintenance_logs`
--

CREATE TABLE `maintenance_logs` (
  `id` int(11) NOT NULL,
  `vehicle_id` int(11) NOT NULL,
  `maintenance_date` date NOT NULL,
  `maintenance_type` varchar(50) DEFAULT 'routine',
  `description` text NOT NULL,
  `labor_cost` decimal(10,2) DEFAULT 0.00,
  `parts_cost` decimal(10,2) DEFAULT 0.00,
  `total_cost` decimal(12,2) NOT NULL,
  `service_center` varchar(200) DEFAULT NULL,
  `next_service_date` date DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `maintenance_logs`
--

INSERT INTO `maintenance_logs` (`id`, `vehicle_id`, `maintenance_date`, `maintenance_type`, `description`, `labor_cost`, `parts_cost`, `total_cost`, `service_center`, `next_service_date`, `created_at`) VALUES
(1, 1, '2026-06-05', 'routine', 'oil change', 1000.00, 0.00, 1000.00, 'Nipun Motors', '2026-06-25', '2026-06-03 08:58:44'),
(3, 5, '2026-06-06', 'emergency', 'oil change', 5000.00, 5000.00, 10000.00, 'MS Motors', '2026-12-06', '2026-06-06 13:32:47'),
(4, 6, '2026-06-01', 'routine', 'Oil change and filter replacement', 5000.00, 8000.00, 13000.00, 'D*MO Motors', '2026-09-01', '2026-06-08 13:40:40'),
(5, 7, '2026-06-07', 'emergency', 'oil change', 8000.00, 12000.00, 20000.00, 'AB Motors', '2028-09-07', '2026-06-08 13:40:40'),
(8, 5, '2026-06-09', 'routine', 'Regular engine oil replacement', 15000.00, 6800.00, 21800.00, 'SL Mortors', '2028-06-10', '2026-06-09 18:45:25');

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `title` varchar(200) NOT NULL,
  `message` text NOT NULL,
  `type` varchar(50) DEFAULT 'info',
  `is_read` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notifications`
--

INSERT INTO `notifications` (`id`, `user_id`, `title`, `message`, `type`, `is_read`, `created_at`) VALUES
(1, 8, 'New Schedule Assigned', 'You have been assigned a new trip on 2026-06-03', 'schedule', 0, '2026-06-03 17:23:18'),
(2, 8, 'New Schedule Assigned', 'You have been assigned a new trip on 2026-06-03', 'schedule', 0, '2026-06-03 18:12:31'),
(3, 6, 'New Schedule Assigned', 'You have been assigned a new trip on 2026-06-04', 'schedule', 0, '2026-06-04 02:19:53'),
(4, 7, 'Booking Confirmed', 'Your booking has been confirmed. Total fare: Rs. 0.0', 'booking', 0, '2026-06-04 02:22:36'),
(5, 7, 'Booking Confirmed', 'Your booking has been confirmed. Total fare: Rs. 0.0', 'booking', 0, '2026-06-04 02:24:54'),
(6, 8, 'New Schedule Assigned', 'You have been assigned a new trip on 2026-06-04', 'schedule', 0, '2026-06-04 09:30:54'),
(7, 8, 'New Schedule Assigned', 'You have been assigned a new trip on 2026-06-04', 'schedule', 0, '2026-06-04 15:04:49'),
(8, 24, 'New Schedule Assigned', 'You have been assigned a new trip on 2026-06-06', 'schedule', 0, '2026-06-06 13:17:02'),
(9, 25, 'New Schedule Assigned', 'You have been assigned a new trip on 2026-06-09', 'schedule', 0, '2026-06-08 13:59:20'),
(10, 6, 'New Schedule Assigned', 'You have been assigned a new trip on 2026-06-10', 'schedule', 0, '2026-06-08 14:00:08'),
(11, 1, 'Booking Confirmed', 'Your booking has been confirmed. Total fare: Rs. 350.0', 'booking', 0, '2026-06-08 14:00:35'),
(12, 8, 'Schedule Updated', 'Your schedule on 2026-06-10 has been updated. Departure: 23:42, Arrival: 15:29', 'schedule', 0, '2026-06-08 18:20:19'),
(13, 6, 'Schedule Removed', 'Your schedule on 2026-06-10 has been reassigned to another driver.', 'schedule', 0, '2026-06-08 18:20:19'),
(14, 24, 'Schedule Updated', 'Your schedule on 2026-06-09 has been updated. Departure: 04:57, Arrival: 06:06', 'schedule', 0, '2026-06-08 18:22:16'),
(15, 25, 'Schedule Removed', 'Your schedule on 2026-06-09 has been reassigned to another driver.', 'schedule', 0, '2026-06-08 18:22:16'),
(16, 6, 'New Schedule Assigned', 'You have been assigned a new trip on 2026-06-09', 'schedule', 0, '2026-06-09 12:25:52'),
(17, 8, 'New Schedule Assigned', 'You have been assigned a new trip on 2026-06-10 at 07:20', 'schedule', 0, '2026-06-09 16:53:15'),
(18, 25, 'Schedule Updated', 'Your schedule on 2026-06-10 has been updated. Departure: 07:40, Arrival: 08:05', 'schedule', 0, '2026-06-09 16:55:40'),
(19, 8, 'Schedule Removed', 'Your schedule on 2026-06-10 has been reassigned to another driver.', 'schedule', 0, '2026-06-09 16:55:41'),
(20, 25, 'Driver Assignment', 'You have been assigned to route \"Kandy - Nuwara Eliya\" on 2026-06-09 at 4:57:00', 'schedule', 0, '2026-06-09 17:35:35'),
(21, 6, 'Driver Assignment', 'You have been assigned to route \"Negombo - Kurunegala\" on 2026-06-10 at 23:42:00', 'schedule', 0, '2026-06-10 06:36:10'),
(22, 6, 'Schedule Updated', 'Your schedule on 2026-06-10 has been updated. Departure: 23:42:00, Arrival: 15:29:00', 'schedule', 0, '2026-06-10 10:03:34'),
(23, 6, 'Schedule Updated', 'Your schedule on 2026-06-10 has been updated. Departure: 23:42:00, Arrival: 15:29:00', 'schedule', 0, '2026-06-10 10:04:25'),
(24, 25, 'New Schedule Assigned', 'You have been assigned a new trip on 2026-06-11', 'schedule', 0, '2026-06-11 16:56:24'),
(25, 25, 'Schedule Updated', 'Your schedule on 2026-06-12 has been updated. Departure: 22:32, Arrival: 04:43', 'schedule', 0, '2026-06-11 16:58:05'),
(26, 1, 'Booking Confirmed', 'Your booking has been confirmed. Total fare: Rs. 1650.0', 'booking', 0, '2026-06-11 16:58:53'),
(27, 24, 'Schedule Updated', 'Your schedule on 2026-06-11 has been updated. Departure: 20:48:00, Arrival: 23:50', 'schedule', 0, '2026-06-11 17:06:30'),
(28, 7, 'Booking Confirmed', 'Your booking has been confirmed. Total fare: Rs. 0.0', 'booking', 0, '2026-06-11 17:25:10'),
(29, 6, 'New Schedule Assigned', 'You have been assigned a new trip on 2026-06-12', 'schedule', 0, '2026-06-12 07:56:08'),
(30, 6, 'Schedule Updated', 'Your schedule on 2026-09-12 has been updated. Departure: 13:29:00, Arrival: 15:25:00', 'schedule', 0, '2026-06-12 09:26:21'),
(31, 6, 'New Schedule Assigned', 'You have been assigned a new trip on 2025-07-09', 'schedule', 0, '2026-06-12 09:28:50'),
(32, 6, 'Schedule Updated', 'Your schedule on 2026-06-03 has been updated. Departure: 15:10:00, Arrival: 15:10:00', 'schedule', 0, '2026-06-12 09:28:53'),
(33, 6, 'New Schedule Assigned', 'You have been assigned a new trip on 2026-06-12', 'schedule', 0, '2026-06-12 10:26:22'),
(34, 8, 'New Schedule Assigned', 'You have been assigned a new trip on 2026-06-12', 'schedule', 0, '2026-06-12 10:28:20'),
(35, 24, 'New Schedule Assigned', 'You have been assigned a new trip on 2026-06-21', 'schedule', 0, '2026-06-13 12:23:25');

-- --------------------------------------------------------

--
-- Table structure for table `role_permissions`
--

CREATE TABLE `role_permissions` (
  `id` int(11) NOT NULL,
  `role` varchar(50) NOT NULL,
  `permission` varchar(100) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `role_permissions`
--

INSERT INTO `role_permissions` (`id`, `role`, `permission`, `created_at`) VALUES
(1, 'admin', 'manage_routes', '2026-06-04 18:54:37'),
(2, 'admin', 'manage_vehicles', '2026-06-04 18:54:37'),
(3, 'admin', 'manage_drivers', '2026-06-04 18:54:37'),
(4, 'admin', 'manage_schedules', '2026-06-04 18:54:37'),
(5, 'admin', 'manage_fuel_logs', '2026-06-04 18:54:37'),
(6, 'admin', 'manage_maintenance', '2026-06-04 18:54:37'),
(7, 'admin', 'manage_users', '2026-06-04 18:54:37'),
(8, 'admin', 'manage_tickets', '2026-06-04 18:54:37'),
(9, 'admin', 'view_all_reports', '2026-06-04 18:54:37'),
(10, 'admin', 'view_dashboard', '2026-06-04 18:54:37'),
(11, 'admin', 'update_profile', '2026-06-04 18:54:37'),
(12, 'admin', 'receive_notifications', '2026-06-04 18:54:37'),
(35, 'driver', 'view_assigned_schedules', '2026-06-04 18:54:37'),
(36, 'driver', 'manage_own_fuel_logs', '2026-06-04 18:54:37'),
(37, 'driver', 'update_live_location', '2026-06-04 18:54:37'),
(38, 'driver', 'view_own_reports', '2026-06-04 18:54:37'),
(39, 'driver', 'view_dashboard', '2026-06-04 18:54:37'),
(40, 'driver', 'update_profile', '2026-06-04 18:54:37'),
(41, 'driver', 'receive_notifications', '2026-06-04 18:54:37'),
(42, 'customer', 'view_routes', '2026-06-04 18:54:37'),
(43, 'customer', 'book_tickets', '2026-06-04 18:54:37'),
(44, 'customer', 'view_own_bookings', '2026-06-04 18:54:37'),
(45, 'customer', 'cancel_own_bookings', '2026-06-04 18:54:37'),
(46, 'customer', 'track_buses', '2026-06-04 18:54:37'),
(47, 'customer', 'create_tickets', '2026-06-04 18:54:37'),
(48, 'customer', 'view_dashboard', '2026-06-04 18:54:37'),
(49, 'customer', 'update_profile', '2026-06-04 18:54:37'),
(50, 'customer', 'receive_notifications', '2026-06-04 18:54:37'),
(67, 'supervisor', 'view_dashboard', '2026-06-08 20:38:34'),
(68, 'supervisor', 'manage_routes', '2026-06-08 20:38:34'),
(69, 'supervisor', 'manage_vehicles', '2026-06-08 20:38:34'),
(70, 'supervisor', 'manage_schedules', '2026-06-08 20:38:34'),
(71, 'supervisor', 'manage_fuel_logs', '2026-06-08 20:38:34'),
(72, 'supervisor', 'manage_maintenance', '2026-06-08 20:38:34'),
(73, 'supervisor', 'view_reports', '2026-06-08 20:38:34'),
(74, 'supervisor', 'manage_tickets', '2026-06-08 20:38:34'),
(75, 'supervisor', 'update_profile', '2026-06-08 20:38:34'),
(76, 'supervisor', 'receive_notifications', '2026-06-08 20:38:34'),
(77, 'supervisor', 'view_drivers', '2026-06-09 12:48:26'),
(89, 'depot_manager', 'view_dashboard', '2026-06-09 15:42:26'),
(90, 'depot_manager', 'create_schedules', '2026-06-09 15:42:26'),
(91, 'depot_manager', 'manage_schedules', '2026-06-09 15:42:26'),
(92, 'depot_manager', 'view_schedules', '2026-06-09 15:42:26'),
(93, 'depot_manager', 'manage_fuel_logs', '2026-06-09 15:42:26'),
(94, 'depot_manager', 'manage_maintenance', '2026-06-09 15:42:26'),
(95, 'depot_manager', 'view_routes', '2026-06-09 15:42:26'),
(96, 'depot_manager', 'view_vehicles', '2026-06-09 15:42:26'),
(97, 'depot_manager', 'view_drivers', '2026-06-09 15:42:26'),
(98, 'depot_manager', 'view_reports', '2026-06-09 15:42:26'),
(99, 'depot_manager', 'update_trip_status', '2026-06-09 15:42:26'),
(100, 'depot_manager', 'update_profile', '2026-06-09 15:42:26'),
(101, 'depot_manager', 'receive_notifications', '2026-06-09 15:42:26'),
(102, 'depot_manager', 'manage_routes', '2026-06-09 16:21:28'),
(103, 'depot_manager', 'delete_routes', '2026-06-09 16:21:28'),
(104, 'depot_manager', 'edit_schedules', '2026-06-09 16:33:28'),
(105, 'depot_manager', 'delete_schedules', '2026-06-09 16:33:28'),
(113, 'depot_manager', 'assign_drivers', '2026-06-09 17:18:30'),
(114, 'depot_manager', 'manage_driver_assignments', '2026-06-09 17:18:30'),
(116, 'depot_manager', 'manage_vehicles', '2026-06-09 17:46:44'),
(117, 'depot_manager', 'assign_vehicles', '2026-06-09 17:46:44'),
(118, 'depot_manager', 'edit_vehicles', '2026-06-09 17:46:44'),
(120, 'depot_manager', 'create_fuel_logs', '2026-06-09 17:59:27'),
(121, 'depot_manager', 'view_fuel_logs', '2026-06-09 17:59:27'),
(123, 'depot_manager', 'create_maintenance', '2026-06-09 18:17:41'),
(124, 'depot_manager', 'edit_maintenance', '2026-06-09 18:17:41'),
(125, 'depot_manager', 'delete_maintenance', '2026-06-09 18:17:41'),
(126, 'depot_manager', 'view_maintenance', '2026-06-09 18:17:41'),
(127, 'admin', 'track_buses', '2026-06-10 06:31:49'),
(128, 'depot_manager', 'track_buses', '2026-06-10 06:31:49'),
(129, 'supervisor', 'track_buses', '2026-06-10 06:31:49'),
(135, 'customer', 'view_schedules', '2026-06-11 17:13:14');

-- --------------------------------------------------------

--
-- Table structure for table `routes`
--

CREATE TABLE `routes` (
  `id` int(11) NOT NULL,
  `route_code` varchar(20) NOT NULL,
  `route_name` varchar(200) NOT NULL,
  `start_point` varchar(200) NOT NULL,
  `end_point` varchar(200) NOT NULL,
  `intermediate_stops` text DEFAULT NULL,
  `total_distance` decimal(10,2) NOT NULL,
  `base_fare` decimal(10,2) DEFAULT 0.00,
  `route_type` varchar(50) DEFAULT 'urban',
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `routes`
--

INSERT INTO `routes` (`id`, `route_code`, `route_name`, `start_point`, `end_point`, `intermediate_stops`, `total_distance`, `base_fare`, `route_type`, `is_active`, `created_at`, `updated_at`) VALUES
(1, 'R-001', 'Matara-Colombo Express', 'Matara', 'Colombo', 'Galle', 100.00, 0.00, 'express', 1, '2026-06-03 08:51:05', '2026-06-03 08:51:05'),
(4, 'R-003', 'Colombo-Kandy', 'Colombo', 'Kandy', 'colombo,Kandy', 110.00, 0.00, 'urban', 1, '2026-06-03 18:11:14', '2026-06-03 18:11:14'),
(5, 'R-004', 'Kataragama-Jaffna', 'Katharagama', 'Jaffna', 'Kataragama,hambantota,Tissa,Ranna,Tangalle,Matara, colombo', 473.00, 0.00, 'express', 1, '2026-06-04 02:18:52', '2026-06-04 02:18:52'),
(6, 'R-005', 'Matara - Dikwalla', 'Dikwalla', 'Matara', 'tgh7yjuki,gfyhuji', 50.00, 0.00, 'express', 1, '2026-06-04 09:29:56', '2026-06-04 09:29:56'),
(8, 'R-002', 'Matara-Galle', 'Matara', 'Galle', 'Matara Central Bus Stand, Nupe Junction, Walgama Junction, Kamburugamuwa Junction, Mirissa, Weligama Bus Stand, Midigama, Ahangama, Koggala, Habaraduwa Bus Stand, Thalpe, Dalawella, Unawatuna, Dewata Junction, Galle Central Bus Station', 44.00, 0.00, 'express', 1, '2026-06-04 15:03:45', '2026-06-04 15:03:45'),
(9, 'R-006', 'Matara- Thangalla', 'Matara', 'Thangalla', 'Matara, Dewinuwara,Kapugama,Gandara,Thalalla,Kottagoda,Dikwalla,Thangalla\r\n', 44.00, 0.00, 'intercity', 1, '2026-06-06 13:07:50', '2026-06-06 13:07:50'),
(10, 'R-007', 'Colombo - Galle Express', 'Colombo', 'Galle', 'Kadawatha, Kalutara, Bentota, Hikkaduwa ', 200.00, 500.00, 'express', 1, '2026-06-08 13:35:54', '2026-06-08 16:41:57'),
(11, 'R-008', 'Kandy - Nuwara Eliya', 'Kandy', 'Nuwara Eliya', 'Peradeniya, Gampola, Hatton', 100.00, 550.00, 'express', 1, '2026-06-08 13:35:54', '2026-06-08 16:44:19'),
(12, 'R-009', 'Negombo - Kurunegala', 'Negombo', 'Kurunegala', 'Katunayake, Gampaha, Nittambuwa', 85.00, 400.00, 'urban', 1, '2026-06-08 13:35:54', '2026-06-08 13:35:54'),
(13, 'R-10', 'Hambantota-Matara', 'Hambantota', 'Matara', 'Ambalangoda,Thangalla,Beliatta,Dikwalla,Wawrukannala,Matara', 80.00, 400.00, 'express', 1, '2026-06-09 11:52:40', '2026-06-09 11:52:40'),
(14, 'R-011', 'Badulla-Ella', 'Badulla', 'Nuwara', 'Bandarawela, Demodara', 25.00, 99.77, 'urban', 1, '2026-06-09 16:23:03', '2026-06-12 08:32:25'),
(15, 'R-012', 'matara - colombo ', 'matara', 'colombo', 'matara', 300.00, 2000.00, 'urban', 1, '2026-06-12 08:34:17', '2026-06-12 08:34:17'),
(16, 'R-013', 'Embilipitiya - Matara', 'Colombo', 'matara', 'colombo - matara', 300.00, 400.00, 'urban', 1, '2026-06-12 09:24:54', '2026-06-12 09:25:21');

-- --------------------------------------------------------

--
-- Table structure for table `schedules`
--

CREATE TABLE `schedules` (
  `id` int(11) NOT NULL,
  `route_id` int(11) NOT NULL,
  `vehicle_id` int(11) NOT NULL,
  `driver_id` int(11) NOT NULL,
  `departure_time` time NOT NULL,
  `arrival_time` time NOT NULL,
  `schedule_date` date NOT NULL,
  `status` varchar(20) DEFAULT 'scheduled',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `schedules`
--

INSERT INTO `schedules` (`id`, `route_id`, `vehicle_id`, `driver_id`, `departure_time`, `arrival_time`, `schedule_date`, `status`, `created_at`) VALUES
(2, 1, 1, 6, '15:10:00', '15:10:00', '2026-06-03', 'on_time', '2026-06-03 09:40:21'),
(4, 1, 2, 8, '22:55:00', '10:53:00', '2026-06-03', 'scheduled', '2026-06-03 17:23:18'),
(5, 1, 1, 6, '10:00:00', '12:00:00', '2026-06-03', 'scheduled', '2026-06-03 17:44:40'),
(6, 4, 1, 8, '23:43:00', '02:08:00', '2026-06-03', 'scheduled', '2026-06-03 18:12:30'),
(7, 5, 4, 6, '07:51:00', '23:54:00', '2026-06-04', 'scheduled', '2026-06-04 02:19:53'),
(10, 8, 2, 8, '20:36:00', '21:34:00', '2026-06-04', 'scheduled', '2026-06-04 15:04:49'),
(11, 9, 6, 24, '20:48:00', '23:50:00', '2026-06-11', 'scheduled', '2026-06-06 13:17:02'),
(15, 11, 2, 25, '22:32:00', '04:43:00', '2026-06-12', 'on_time', '2026-06-08 13:59:20'),
(17, 13, 6, 6, '18:55:00', '20:00:00', '2026-06-09', 'scheduled', '2026-06-09 12:25:52'),
(19, 4, 6, 25, '22:32:00', '09:26:00', '2026-06-11', 'scheduled', '2026-06-11 16:56:24'),
(21, 1, 1, 6, '16:00:00', '17:58:00', '2025-07-09', 'delayed', '2026-06-12 09:28:50');

-- --------------------------------------------------------

--
-- Table structure for table `support_tickets`
--

CREATE TABLE `support_tickets` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `ticket_number` varchar(20) NOT NULL,
  `subject` varchar(200) NOT NULL,
  `message` text NOT NULL,
  `status` varchar(20) DEFAULT 'open',
  `priority` varchar(20) DEFAULT 'normal',
  `admin_response` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('admin','depot_manager','supervisor','driver','customer') DEFAULT 'customer',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `is_active` tinyint(1) DEFAULT 1,
  `last_login` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `first_name`, `last_name`, `username`, `email`, `phone`, `address`, `password_hash`, `role`, `created_at`, `is_active`, `last_login`) VALUES
(1, 'Admin', '123', 'admin', 'admin@gmail.com', NULL, NULL, 'scrypt:32768:8:1$DmjUnrsWCgH3zqpT$5fb6b27d04d4747a02c79dbc64ce939e53655b83fd59a6138c577379a57b8a21a56535f6a98d44335103941ee6c6f88edce72606ce22c9810496891e71f016da', 'admin', '2026-06-03 08:05:08', 1, '2026-06-15 13:45:40'),
(2, 'Binidu', 'Ranasinghe', 'binidu', 'rbinidu@gmail.com', NULL, NULL, 'scrypt:32768:8:1$bO3Cr6Wx4hbEAVVW$bea796125d2d25611542f9a5cf0c6006dd8c8389bee538bc1e1176a0404d81e3075cd56b8642a00b2d35989a98ebbc383e909c8d176a9ddb9882616886e07851', 'customer', '2026-06-03 08:05:48', 1, NULL),
(5, 'fghh', 'fghjkhg', 'hjkhgf', 'binidu@gmail.com', NULL, NULL, 'scrypt:32768:8:1$581QbMQNIxM295Vj$d02c54da225dda53d441784966c6278f17889cc7771252ec7d7f67284d2e34cb838b8a9cbed173d07eb939fa990e8ee04679a1fcc1c7bd9c4b0fd8c59d91b763', 'customer', '2026-06-03 08:40:55', 1, NULL),
(6, 'Bagya', 'Rishani', 'rishu', 'rishu@gmail.com', '0777858585', NULL, 'scrypt:32768:8:1$qY6ys9jijcDWOATG$fa84f121ca7265d98087a1e1242e736cdaa3f68116e0cd1be0ce442ff3cfa46e88163dfe9a43ce192cca7bdf77870fba99bb5296477b8b86a79ef786ed582f47', 'driver', '2026-06-03 09:03:03', 1, '2026-06-15 15:49:03'),
(7, 'shehara', 'nethmi', 'nethmi', 'nethmi@gmail.com', '0777481542', 'Kamburugamuwa', 'scrypt:32768:8:1$YgOi895y3NOfwfoV$78fca6f746ed8ff11d45e535a639c192133b19b82e6560e0c954becc663341338043fe026a172e88abda8f27e78ff0e3af8f5cbe610aef267b997f5852bfda42', 'customer', '2026-06-03 10:27:51', 1, '2026-06-15 13:33:09'),
(8, 'Sewwandi', 'Mahadurage', 'sewwandi', 'sew@gmail.com', '0777123456', NULL, 'scrypt:32768:8:1$bsi2i32n7XfgMaey$084c3dc2d4a759446277dff17d11be19bfff840c0da4bebc3f090583afa5ad8837052fa1a596d593e55a01379491c6797d99b8b7ceb70a268f4ab440cbed122f', 'driver', '2026-06-03 17:20:50', 1, '2026-06-04 19:17:08'),
(22, 'Depot', 'Manager', 'manager', 'manager@srmss.lk', NULL, NULL, 'scrypt:32768:8:1$DmjUnrsWCgH3zqpT$5fb6b27d04d4747a02c79dbc64ce939e53655b83fd59a6138c577379a57b8a21a56535f6a98d44335103941ee6c6f88edce72606ce22c9810496891e71f016da', 'depot_manager', '2026-06-05 07:00:38', 1, '2026-06-15 15:44:24'),
(23, 'Super', 'Visor', 'supervisor', 'supervisor@srmss.lk', NULL, NULL, 'scrypt:32768:8:1$DmjUnrsWCgH3zqpT$5fb6b27d04d4747a02c79dbc64ce939e53655b83fd59a6138c577379a57b8a21a56535f6a98d44335103941ee6c6f88edce72606ce22c9810496891e71f016da', 'supervisor', '2026-06-05 07:00:38', 1, '2026-06-15 15:00:29'),
(24, 'Danushka', 'Rathnayaka', 'danu', 'danushka@gmail.com', '', NULL, 'scrypt:32768:8:1$3l5yd4okpbHXZ0KH$0847e3e955047a8c1cd4cea467344c2863b08e7e82243b31e5eb254c54a42d5d38de2df5f9878ea976b8edcdfbe5ec750be1af7b36909f9d5298b5634648afde', 'driver', '2026-06-06 13:12:47', 1, '2026-06-08 17:35:57'),
(25, 'Kamal', 'Perera', 'kamal', 'kamal@driver.com', '0711234567', 'Colombo', 'scrypt:32768:8:1$jz8f1R9vxlIrfmVm$6d40b6fce1a6f5683c5391835392aa3805f4191126b1c8c21e6c544cf31b3db9a2b98ca0ded1feae79d00c17653d32cf16052c80cb107fbf68fba6c6f31e177f', 'driver', '2026-06-08 13:25:12', 1, '2026-06-12 05:13:36'),
(27, 'Nimal', 'Silva', 'silva', 'silva@gmail.com', '', NULL, 'scrypt:32768:8:1$iglJnuCSKLVM3iph$fbab1932a39f825d32fc53a7a073d725513cd5ab377e8790f762f2237343622dbbd1ace0de7c14c926ba438fcaece86111a1e9ed82e3901604bd631fa2cde03c', 'driver', '2026-06-08 13:32:11', 1, '2026-06-08 13:33:36'),
(28, 'Nadee', 'Shashikala', 'nadee', 'nadee@gmail.com', '', NULL, 'scrypt:32768:8:1$GnLJHH6viFY01JXp$ea467e817ed35d6e430c11f9a5bf699f624ab4b47c018eb246fae3b5d5b0f3c3b8ab1166ef06dc4ac464e0fc1a587042b97a6f1aff1c918cf64f2328f0d1ba7b', 'customer', '2026-06-08 13:43:21', 1, '2026-06-08 14:00:56'),
(34, 'chamali', 'kavindi', 'chamali', 'chamali@gmail.com', '', NULL, 'scrypt:32768:8:1$U0Co2iF2iuoL8cgh$9e9de6d8a1305d02c72fe118ee287b146ae086f4925c3a56faa76bc9603e29f13defb9095893a7b8c391b77fc16d5003b61b799adc4e254138b6cac3128e72e9', 'customer', '2026-06-13 12:01:42', 1, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `user_activity_log`
--

CREATE TABLE `user_activity_log` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `action` varchar(200) NOT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_activity_log`
--

INSERT INTO `user_activity_log` (`id`, `user_id`, `action`, `ip_address`, `user_agent`, `created_at`) VALUES
(1, 7, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-04 18:55:11'),
(2, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-04 18:55:49'),
(3, 6, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-04 18:58:35'),
(4, 6, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-04 19:01:10'),
(5, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-04 19:08:33'),
(6, 6, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-04 19:15:56'),
(7, 6, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-04 19:16:00'),
(8, 7, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-04 19:16:08'),
(9, 7, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-04 19:16:13'),
(10, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-04 19:16:31'),
(11, 8, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-04 19:17:08'),
(12, 8, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-04 19:17:40'),
(13, 7, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-04 19:37:15'),
(14, 7, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-04 19:44:33'),
(15, 7, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-04 19:45:03'),
(16, 7, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-04 19:45:20'),
(17, 7, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-04 19:45:40'),
(18, 7, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-04 19:48:14'),
(19, 7, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-04 19:48:19'),
(20, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-04 19:48:32'),
(21, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-05 04:59:45'),
(22, 6, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-05 05:12:02'),
(23, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-05 05:18:03'),
(24, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-05 05:21:43'),
(25, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-05 05:22:19'),
(26, 6, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-05 05:26:37'),
(27, 7, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-05 05:27:55'),
(28, 7, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-05 06:13:58'),
(29, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-05 07:09:36'),
(30, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-05 07:11:00'),
(31, 22, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-05 07:11:55'),
(32, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-05 07:12:14'),
(33, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-05 07:13:57'),
(34, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-05 07:26:11'),
(35, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-05 07:26:29'),
(36, 22, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-05 07:26:50'),
(37, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-05 07:26:59'),
(38, 23, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-05 07:27:35'),
(39, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-05 07:27:44'),
(40, 1, 'Added fuel log for vehicle ID: 2', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-05 07:36:07'),
(41, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-06 12:54:01'),
(42, 6, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-06 12:54:23'),
(43, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-06 12:54:43'),
(44, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-06 12:55:42'),
(45, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-06 12:56:28'),
(46, 22, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-06 12:57:06'),
(47, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-06 12:58:05'),
(48, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-06 12:58:18'),
(49, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-06 12:59:58'),
(50, 22, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-06 13:05:00'),
(51, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-06 13:05:10'),
(52, 1, 'Added route: R-006', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-06 13:07:50'),
(53, 1, 'Added vehicle: NB 1459', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-06 13:10:34'),
(54, 1, 'Added driver: danu', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-06 13:12:47'),
(55, 24, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-06 13:14:23'),
(56, 24, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-06 13:15:58'),
(57, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-06 13:16:08'),
(58, 1, 'Added schedule for driver ID: 24', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-06 13:17:02'),
(59, 24, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-06 13:17:20'),
(60, 24, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-06 13:25:04'),
(61, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-06 13:25:13'),
(62, 1, 'Added maintenance for vehicle ID: 5', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-06 13:30:08'),
(63, 1, 'Deleted maintenance log ID: 2', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-06 13:31:17'),
(64, 1, 'Added maintenance for vehicle ID: 5', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-06 13:32:47'),
(65, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-06 14:32:30'),
(66, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-06 16:19:13'),
(67, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 10:09:08'),
(68, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 10:09:26'),
(69, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 11:15:06'),
(70, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 13:14:29'),
(71, 1, 'Added driver: silva', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 13:32:11'),
(72, 27, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 13:33:36'),
(73, 27, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 13:33:46'),
(74, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 13:33:57'),
(75, 23, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 13:34:05'),
(76, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 13:34:29'),
(77, 22, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 13:36:11'),
(78, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 13:36:27'),
(79, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 13:41:54'),
(80, 28, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 13:43:32'),
(81, 28, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 13:46:50'),
(82, 7, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 13:46:57'),
(83, 7, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 13:57:58'),
(84, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 13:58:10'),
(85, 1, 'Added schedule for driver ID: 25', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 13:59:20'),
(86, 1, 'Added schedule for driver ID: 6', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 14:00:08'),
(87, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 14:00:45'),
(88, 28, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 14:00:56'),
(89, 28, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 14:01:52'),
(90, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 14:02:04'),
(91, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 14:10:05'),
(92, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 16:07:44'),
(93, 1, 'Updated route: R-007 (ID: 10)', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 16:15:22'),
(94, 1, 'Updated route: R-007 (ID: 10)', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 16:41:57'),
(95, 1, 'Updated route: R-008 (ID: 11)', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 16:44:19'),
(96, 1, 'Updated vehicle: NB 4725 (ID: 2)', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 16:47:12'),
(97, 7, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 17:00:12'),
(98, 7, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 17:00:35'),
(99, 24, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 17:00:54'),
(100, 24, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 17:01:22'),
(101, 24, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 17:01:32'),
(102, 24, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 17:02:26'),
(103, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 17:05:18'),
(104, 1, 'Reset password for driver ID: 24', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 17:35:16'),
(105, 24, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 17:35:57'),
(106, 24, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 17:58:02'),
(107, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 17:58:27'),
(108, 1, 'Updated driver ID: 8', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 17:58:52'),
(109, 1, 'Updated driver ID: 6', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 18:00:04'),
(110, 1, 'Updated schedule ID: 16', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 18:20:19'),
(111, 1, 'Updated schedule ID: 15', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 18:22:16'),
(112, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 18:23:29'),
(113, 6, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 18:23:40'),
(114, 6, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 18:38:59'),
(115, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 18:39:13'),
(116, 1, 'Updated maintenance log ID: 5', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 19:03:25'),
(117, 1, 'Updated maintenance log ID: 5', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 19:05:45'),
(118, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 19:06:50'),
(119, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 19:07:01'),
(120, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 19:15:39'),
(121, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 19:15:57'),
(122, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 19:16:31'),
(123, 22, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 19:16:36'),
(124, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 19:16:46'),
(125, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 20:13:31'),
(126, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 20:18:14'),
(127, 23, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 20:39:15'),
(128, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 20:39:26'),
(129, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 20:40:24'),
(130, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 20:40:33'),
(131, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 20:42:17'),
(132, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-08 20:43:31'),
(133, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 11:48:19'),
(134, 23, 'Added route: R-10', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 11:52:40'),
(135, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 11:53:09'),
(136, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 11:54:19'),
(137, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 11:54:30'),
(138, 23, 'Added vehicle: NB 7841', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 11:55:29'),
(139, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 12:10:52'),
(140, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 12:24:02'),
(141, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 12:24:11'),
(142, 23, 'Added schedule for driver ID: 6', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 12:25:53'),
(143, 6, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 12:27:12'),
(144, 6, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 12:28:11'),
(145, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 12:28:21'),
(146, 23, 'Added fuel log for vehicle ID: 7', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 12:30:33'),
(147, 23, 'Added maintenance for vehicle ID: 4', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 12:35:18'),
(148, 23, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 12:36:22'),
(149, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 12:36:32'),
(150, 23, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 12:58:41'),
(151, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 12:58:51'),
(152, 22, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 13:02:59'),
(153, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 13:03:09'),
(154, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 13:46:25'),
(155, 23, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 14:06:25'),
(156, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 14:06:40'),
(157, 22, 'Added route: R-011', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 16:23:03'),
(158, 22, 'Updated route: R-011 (ID: 14)', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 16:25:17'),
(159, 22, 'Created schedule for driver ID: 8', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 16:53:15'),
(160, 22, 'Updated schedule ID: 18', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 16:55:41'),
(161, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 17:19:07'),
(162, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 17:19:36'),
(163, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 17:24:43'),
(164, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 17:24:53'),
(165, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 17:24:58'),
(166, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 17:25:07'),
(167, 23, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 17:25:34'),
(168, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 17:25:43'),
(169, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 17:27:54'),
(170, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 17:31:20'),
(171, 22, 'Assigned driver 25 to schedule 15', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 17:35:35'),
(172, 22, 'Assigned vehicle 2 to schedule 15', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 17:51:08'),
(173, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 17:59:53'),
(174, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 18:00:36'),
(175, 22, 'Added fuel log for vehicle ID: 9', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 18:02:25'),
(176, 22, 'Added maintenance for vehicle ID: 5', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 18:42:28'),
(177, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 18:43:32'),
(178, 1, 'Deleted maintenance log ID: 7', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 18:44:13'),
(179, 1, 'Added maintenance for vehicle ID: 5', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 18:45:25'),
(180, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 18:46:08'),
(181, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', '2026-06-09 18:46:35'),
(182, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 04:50:51'),
(183, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 04:51:10'),
(184, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 04:51:46'),
(185, 23, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 06:18:31'),
(186, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 06:19:05'),
(187, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 06:22:37'),
(188, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 06:22:49'),
(189, 23, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 06:23:24'),
(190, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 06:23:56'),
(191, 22, 'Assigned driver 6 to schedule 16', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 06:36:10'),
(192, 22, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 06:40:08'),
(193, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 06:40:22'),
(194, 23, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 06:47:34'),
(195, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 06:47:47'),
(196, 22, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 06:59:43'),
(197, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 06:59:51'),
(198, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 07:22:32'),
(199, 7, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 07:22:50'),
(200, 7, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 07:35:19'),
(201, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 07:35:30'),
(202, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 07:48:04'),
(203, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 07:48:12'),
(204, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 08:11:47'),
(205, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 08:11:57'),
(206, 23, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 08:12:32'),
(207, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 08:12:40'),
(208, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 08:18:36'),
(209, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 08:18:45'),
(210, 23, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 08:19:02'),
(211, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 08:19:13'),
(212, 22, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 08:20:27'),
(213, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 08:20:36'),
(214, 22, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 08:26:48'),
(215, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 08:27:00'),
(216, 22, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 08:31:09'),
(217, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 08:31:22'),
(218, 22, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 08:38:48'),
(219, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 08:38:58'),
(220, 22, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 08:50:27'),
(221, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 08:50:38'),
(222, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 08:51:05'),
(223, 22, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 08:58:43'),
(224, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 08:58:51'),
(225, 22, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 09:10:50'),
(226, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 09:10:59'),
(227, 23, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 09:16:41'),
(228, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 09:16:58'),
(229, 22, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 09:29:18'),
(230, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 09:29:29'),
(231, 22, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 10:00:52'),
(232, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 10:01:07'),
(233, 1, 'Updated schedule ID: 16', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 10:03:34'),
(234, 1, 'Updated schedule ID: 16', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 10:04:25'),
(235, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 10:06:04'),
(236, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 10:06:24'),
(237, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 10:09:04'),
(238, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 10:09:34'),
(239, 23, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 10:12:21'),
(240, 7, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-10 10:12:34'),
(241, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-11 13:37:52'),
(242, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-11 13:40:09'),
(243, 7, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-11 13:40:28'),
(244, 7, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-11 16:12:58'),
(245, 7, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-11 16:47:28'),
(246, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-11 16:55:24'),
(247, 1, 'Added schedule for driver ID: 25', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-11 16:56:24'),
(248, 1, 'Updated schedule ID: 15', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-11 16:58:05'),
(249, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-11 17:01:21'),
(250, 7, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-11 17:01:36'),
(251, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-11 17:05:51'),
(252, 1, 'Updated schedule ID: 11', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-11 17:06:30'),
(253, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-11 17:06:43'),
(254, 7, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-11 17:06:56'),
(255, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 04:53:56'),
(256, 1, 'Reset password for driver ID: 25', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 05:13:07'),
(257, 25, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 05:13:36'),
(258, 25, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 05:15:48'),
(259, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 05:15:58'),
(260, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 06:01:51'),
(261, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 06:02:11'),
(262, 22, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 06:06:26'),
(263, 6, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 06:06:42'),
(264, 6, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 06:10:25'),
(265, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 06:10:34'),
(266, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 06:58:48'),
(267, 7, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 06:58:59'),
(268, 7, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 07:17:15'),
(269, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 07:17:31'),
(270, 22, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 07:18:29'),
(271, 7, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 07:18:38'),
(272, 7, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 07:19:25'),
(273, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 07:19:37'),
(274, 22, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 07:44:32'),
(275, 6, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 07:44:46'),
(276, 6, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 07:45:37'),
(277, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 07:45:46');
INSERT INTO `user_activity_log` (`id`, `user_id`, `action`, `ip_address`, `user_agent`, `created_at`) VALUES
(278, 22, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 07:46:11'),
(279, 6, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 07:46:26'),
(280, 6, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 07:48:03'),
(281, 6, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 07:48:30'),
(282, 6, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 07:54:58'),
(283, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 07:55:07'),
(284, 1, 'Added schedule for driver ID: 6', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 07:56:08'),
(285, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 07:56:13'),
(286, 6, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 07:56:27'),
(287, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 07:57:17'),
(288, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 07:59:25'),
(289, 6, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 07:59:44'),
(290, 6, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 08:19:03'),
(291, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 08:19:11'),
(292, 22, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 08:19:15'),
(293, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 08:22:09'),
(294, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 08:22:19'),
(295, 7, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 08:25:46'),
(296, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 08:26:56'),
(297, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 08:27:28'),
(298, 23, 'Updated route: R-011 (ID: 14)', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 08:28:25'),
(299, 23, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 08:28:37'),
(300, 23, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 08:28:47'),
(301, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 08:28:58'),
(302, 23, 'Updated route: R-011 (ID: 14)', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 08:32:26'),
(303, 23, 'Added route: R-012', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 08:34:17'),
(304, 23, 'Deleted fuel log ID: 11', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 08:34:58'),
(305, 23, 'Deleted fuel log ID: 15', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 08:35:54'),
(306, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 09:19:11'),
(307, 23, 'Added route: R-013', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 09:24:54'),
(308, 23, 'Updated route: R-013 (ID: 16)', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 09:25:21'),
(309, 23, 'Updated schedule ID: 20', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 09:26:21'),
(310, 23, 'Added schedule for driver ID: 6', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 09:28:50'),
(311, 23, 'Updated schedule ID: 2', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 09:28:53'),
(312, 23, 'Updated vehicle: NB 7846 (ID: 9)', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 09:30:18'),
(313, 23, 'Added vehicle: AS - 2453', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 09:31:06'),
(314, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 09:47:09'),
(315, 23, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 10:07:29'),
(316, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 10:07:42'),
(317, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 10:10:21'),
(318, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 10:11:16'),
(319, 1, 'Added schedule for driver ID: 6', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 10:26:22'),
(320, 1, 'Added schedule for driver ID: 8', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 10:28:20'),
(321, 1, 'Added fuel log for vehicle ID: 2', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 10:31:45'),
(322, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 10:37:20'),
(323, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 10:38:38'),
(324, 23, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 10:40:18'),
(325, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 10:40:27'),
(326, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 10:49:29'),
(327, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 10:52:08'),
(328, 6, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 11:02:44'),
(329, 6, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 11:17:32'),
(330, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 11:17:45'),
(331, 1, 'Added maintenance for vehicle ID: 4', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-12 11:20:57'),
(332, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-13 11:16:03'),
(333, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-13 11:25:27'),
(334, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-13 11:25:35'),
(335, 22, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-13 11:27:50'),
(336, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-13 11:28:11'),
(337, 23, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-13 11:36:23'),
(338, 7, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-13 11:36:33'),
(339, 7, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-13 11:39:40'),
(340, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-13 11:39:50'),
(341, 22, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-13 11:59:11'),
(342, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-13 11:59:23'),
(343, 1, 'Added user: chamali', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-13 12:01:42'),
(344, 1, 'Added route: R-016', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-13 12:21:49'),
(345, 1, 'Added schedule for driver ID: 24', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-13 12:23:25'),
(346, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-13 13:22:42'),
(347, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-13 15:11:35'),
(348, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-13 16:09:49'),
(349, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-13 16:09:59'),
(350, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-14 05:50:24'),
(351, 1, 'Added route: R-018', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-14 05:51:10'),
(352, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-14 05:54:24'),
(353, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-14 05:58:39'),
(354, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-14 06:17:35'),
(355, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-14 06:18:46'),
(356, 7, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-14 06:18:56'),
(357, 7, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-14 06:19:27'),
(358, 6, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-14 06:19:38'),
(359, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 02:04:43'),
(360, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 02:17:03'),
(361, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 02:17:12'),
(362, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 02:24:32'),
(363, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 02:24:56'),
(364, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 05:05:56'),
(365, 22, 'Updated route: R-018 (ID: 18)', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 05:14:48'),
(366, 22, 'Updated route: R-018 (ID: 18)', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 05:22:13'),
(367, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 07:24:44'),
(368, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 08:42:00'),
(369, 1, 'Added route: R-019', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 08:44:04'),
(370, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 08:53:42'),
(371, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 08:58:57'),
(372, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 13:10:13'),
(373, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 13:13:57'),
(374, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 13:18:35'),
(375, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 13:21:14'),
(376, 1, 'Deleted route ID: 19', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 13:22:43'),
(377, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 13:24:12'),
(378, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 13:26:43'),
(379, 1, 'Deleted route ID: 18', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 13:28:01'),
(380, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 13:32:43'),
(381, 7, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 13:33:09'),
(382, 7, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 13:33:57'),
(383, 1, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 13:45:40'),
(384, 1, 'Deleted route ID: 17', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 13:47:05'),
(385, 1, 'Deleted vehicle ID: 10', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 13:47:53'),
(386, 1, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 14:02:01'),
(387, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 14:02:22'),
(388, 23, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 14:02:27'),
(389, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 14:15:56'),
(390, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 14:20:41'),
(391, 23, 'Deleted fuel log ID: 17', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 14:23:56'),
(392, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 14:39:55'),
(393, 23, 'Deleted fuel log ID: 16', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 14:43:07'),
(394, 23, 'Deleted maintenance log ID: 9', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 14:43:58'),
(395, 23, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 15:00:29'),
(396, 23, 'Deleted maintenance log ID: 6', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 15:04:18'),
(397, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 15:11:43'),
(398, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 15:28:24'),
(399, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 15:33:26'),
(400, 22, 'Updated vehicle: NB 7846 (ID: 9)', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 15:35:27'),
(401, 22, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 15:37:48'),
(402, 6, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 15:38:00'),
(403, 22, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 15:44:24'),
(404, 22, 'User logged out', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 15:48:43'),
(405, 6, 'User logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', '2026-06-15 15:49:03');

-- --------------------------------------------------------

--
-- Table structure for table `vehicles`
--

CREATE TABLE `vehicles` (
  `id` int(11) NOT NULL,
  `vehicle_code` varchar(20) NOT NULL,
  `registration_number` varchar(50) NOT NULL,
  `vehicle_type` varchar(50) DEFAULT 'standard',
  `seating_capacity` int(11) NOT NULL,
  `fuel_type` varchar(20) DEFAULT 'diesel',
  `status` varchar(20) DEFAULT 'available',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `vehicles`
--

INSERT INTO `vehicles` (`id`, `vehicle_code`, `registration_number`, `vehicle_type`, `seating_capacity`, `fuel_type`, `status`, `created_at`, `updated_at`) VALUES
(1, 'BUS-001', 'NB 7125', 'standard', 52, 'diesel', 'available', '2026-06-03 08:45:35', '2026-06-03 08:45:35'),
(2, 'NB 4725', 'SP 0578', 'mini', 45, 'diesel', 'in_use', '2026-06-03 17:22:07', '2026-06-09 17:51:08'),
(4, 'NB 7812', 'SP 7415', 'standard', 45, 'diesel', 'maintenance', '2026-06-04 02:15:44', '2026-06-09 12:35:18'),
(5, 'NB 1459', 'SP 1452', 'double_decker', 45, 'diesel', 'maintenance', '2026-06-06 13:10:34', '2026-06-06 13:30:08'),
(6, 'BUS-006', 'WP-1234', 'standard', 45, 'diesel', 'in_use', '2026-06-08 13:36:54', '2026-06-09 16:53:15'),
(7, 'BUS-007', 'WP-5678', 'double_decker', 70, 'diesel', 'maintenance', '2026-06-08 13:36:54', '2026-06-08 19:03:25'),
(8, 'BUS-008', 'NB-9876', 'standard', 52, 'diesel', 'in_use', '2026-06-08 13:36:54', '2026-06-08 13:36:54'),
(9, 'NB 7846', 'SP 2147', 'double_decker', 33, 'petrol', 'available', '2026-06-09 11:55:29', '2026-06-12 09:30:18');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `schedule_id` (`schedule_id`);

--
-- Indexes for table `driver_locations`
--
ALTER TABLE `driver_locations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `driver_id` (`driver_id`),
  ADD KEY `schedule_id` (`schedule_id`);

--
-- Indexes for table `fuel_logs`
--
ALTER TABLE `fuel_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `vehicle_id` (`vehicle_id`);

--
-- Indexes for table `maintenance_logs`
--
ALTER TABLE `maintenance_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `vehicle_id` (`vehicle_id`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `role_permissions`
--
ALTER TABLE `role_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_role_permission` (`role`,`permission`);

--
-- Indexes for table `routes`
--
ALTER TABLE `routes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `route_code` (`route_code`);

--
-- Indexes for table `schedules`
--
ALTER TABLE `schedules`
  ADD PRIMARY KEY (`id`),
  ADD KEY `route_id` (`route_id`),
  ADD KEY `vehicle_id` (`vehicle_id`),
  ADD KEY `driver_id` (`driver_id`);

--
-- Indexes for table `support_tickets`
--
ALTER TABLE `support_tickets`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ticket_number` (`ticket_number`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `user_activity_log`
--
ALTER TABLE `user_activity_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `vehicles`
--
ALTER TABLE `vehicles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `vehicle_code` (`vehicle_code`),
  ADD UNIQUE KEY `registration_number` (`registration_number`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bookings`
--
ALTER TABLE `bookings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `driver_locations`
--
ALTER TABLE `driver_locations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `fuel_logs`
--
ALTER TABLE `fuel_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `maintenance_logs`
--
ALTER TABLE `maintenance_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT for table `role_permissions`
--
ALTER TABLE `role_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=146;

--
-- AUTO_INCREMENT for table `routes`
--
ALTER TABLE `routes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `schedules`
--
ALTER TABLE `schedules`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `support_tickets`
--
ALTER TABLE `support_tickets`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `user_activity_log`
--
ALTER TABLE `user_activity_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=406;

--
-- AUTO_INCREMENT for table `vehicles`
--
ALTER TABLE `vehicles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bookings`
--
ALTER TABLE `bookings`
  ADD CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`schedule_id`) REFERENCES `schedules` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `driver_locations`
--
ALTER TABLE `driver_locations`
  ADD CONSTRAINT `driver_locations_ibfk_1` FOREIGN KEY (`driver_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `driver_locations_ibfk_2` FOREIGN KEY (`schedule_id`) REFERENCES `schedules` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `fuel_logs`
--
ALTER TABLE `fuel_logs`
  ADD CONSTRAINT `fuel_logs_ibfk_1` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `maintenance_logs`
--
ALTER TABLE `maintenance_logs`
  ADD CONSTRAINT `maintenance_logs_ibfk_1` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `notifications`
--
ALTER TABLE `notifications`
  ADD CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `schedules`
--
ALTER TABLE `schedules`
  ADD CONSTRAINT `schedules_ibfk_1` FOREIGN KEY (`route_id`) REFERENCES `routes` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `schedules_ibfk_2` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `schedules_ibfk_3` FOREIGN KEY (`driver_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `support_tickets`
--
ALTER TABLE `support_tickets`
  ADD CONSTRAINT `support_tickets_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `user_activity_log`
--
ALTER TABLE `user_activity_log`
  ADD CONSTRAINT `user_activity_log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
