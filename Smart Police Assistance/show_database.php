<?php
// Database connection parameters
$host = "localhost";
$port = "3300"; // Change to your MySQL port if different
$dbname = "name"; // Change to your database name
$username = "root"; // Change to your MySQL username
$password = "1234"; // Change to your MySQL password

try {
    // Connect to MySQL database
    $db_connection = new PDO("mysql:host=$host;port=$port;dbname=$dbname", $username, $password);
    $db_connection->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Fetch data from the distress_signals table
    $query = "SELECT * FROM distress_signals";
    $statement = $db_connection->prepare($query);
    $statement->execute();
    $data = $statement->fetchAll(PDO::FETCH_ASSOC);

    // Close the database connection
    $db_connection = null;

    // Send JSON response
    header('Content-Type: application/json');
    echo json_encode($data);
} catch (PDOException $e) {
    // Handle database connection errors
    echo "Error: " . $e->getMessage();
}
?>
