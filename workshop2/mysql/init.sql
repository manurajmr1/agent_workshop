-- Travel-related tables
CREATE TABLE flight_status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flight_number VARCHAR(10) NOT NULL UNIQUE,
    status VARCHAR(50) NOT NULL
);

CREATE TABLE hotels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    location VARCHAR(100) NOT NULL,
    hotel_name VARCHAR(200) NOT NULL,
    stars INT NOT NULL,
    description TEXT
);

CREATE TABLE travel_advice (
    id INT AUTO_INCREMENT PRIMARY KEY,
    location VARCHAR(100) NOT NULL,
    advice TEXT NOT NULL
);

-- Insert flight status data
INSERT INTO flight_status (flight_number, status) VALUES
('AA123', 'On time'),
('DL456', 'Delayed'),
('UA789', 'Cancelled');

-- Insert hotel data
INSERT INTO hotels (location, hotel_name, stars, description) VALUES
('New York', 'The Plaza', 5, 'Top hotel in New York: The Plaza - 5 stars'),
('Los Angeles', 'The Beverly Hills Hotel', 5, 'Top hotel in Los Angeles: The Beverly Hills Hotel - 5 stars'),
('Chicago', 'The Langham', 5, 'Top hotel in Chicago: The Langham - 5 stars');

-- Insert travel advice data
INSERT INTO travel_advice (location, advice) VALUES
('New York', 'Travel advice for New York: Visit Central Park and Times Square.'),
('Los Angeles', 'Travel advice for Los Angeles: Check out Hollywood and Santa Monica Pier.'),
('Chicago', 'Travel advice for Chicago: Don\'t miss the Art Institute and Millennium Park.');
