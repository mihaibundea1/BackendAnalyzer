-- Selectează baza de date
USE myapp;

-- Creează tabela pentru utilizatori
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    type ENUM('patient', 'doctor', 'admin') NOT NULL,
	mfa_secret VARCHAR(255) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Crearea tabelei `investigations`
CREATE TABLE investigations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    image_path VARCHAR(255) NOT NULL,
    diagnostic TEXT,
    description TEXT,
    doctor_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES users(id) ON DELETE SET NULL
);

-- (Opțional) Crearea tabelei `patients_doctors` pentru relația pacient-medic
CREATE TABLE patients_doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Verifică dacă utilizatorul 'admin' există și, dacă nu, creează-l
CREATE USER IF NOT EXISTS 'admin'@'%' IDENTIFIED BY 'admin_password';

-- Atribuie toate privilegiile pe baza de date 'myapp' pentru utilizatorul 'admin'
GRANT ALL PRIVILEGES ON myapp.* TO 'admin'@'%' WITH GRANT OPTION;

-- Permite conectarea de pe orice host
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'%' IDENTIFIED BY 'admin_password' WITH GRANT OPTION;

-- Aplică modificările
FLUSH PRIVILEGES;

-- Adaugă utilizatorul 'admin' în tabela 'users' cu parola criptată folosind SHA2
-- Adăugare utilizator admin
INSERT INTO users (username, email, password_hash, type)
VALUES 
    ('admin', 'mihaibundea1@gmail.com', SHA2('admin', 256), 'admin');
