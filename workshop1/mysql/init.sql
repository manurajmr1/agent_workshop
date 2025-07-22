-- Sample sales order schema and data
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    product VARCHAR(100),
    amount DECIMAL(10,2),
    order_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO users (name, email) VALUES
('Alice', 'alice@example.com'),
('Bob', 'bob@example.com'),
('Charlie', 'charlie@example.com');

INSERT INTO orders (user_id, product, amount, order_date) VALUES
(1, 'Laptop', 1200.00, '2024-06-01'),
(2, 'Phone', 800.00, '2024-06-02'),
(1, 'Mouse', 25.00, '2024-06-03'),
(3, 'Monitor', 300.00, '2024-06-04');
