CREATE TABLE patients (
    id INT IDENTITY(1,1) PRIMARY KEY, -- SERIALをIDENTITYに置き換え
    name VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    diagnosis_date DATE
);

CREATE TABLE medical_records (
    id INT IDENTITY(1,1) PRIMARY KEY, -- SERIALをIDENTITYに置き換え
    patient_id INT REFERENCES patients(id),
    diagnosis VARCHAR(255),
    diagnosis_date DATE
);

CREATE TABLE billing (
    id INT IDENTITY(1,1) PRIMARY KEY, -- SERIALをIDENTITYに置き換え
    patient_id INT REFERENCES patients(id),
    amount NUMERIC(10, 2),
    payment_date DATE
);
