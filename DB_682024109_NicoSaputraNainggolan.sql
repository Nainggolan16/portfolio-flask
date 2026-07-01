CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,

    nama_lengkap VARCHAR(100),
    nama_panggilan VARCHAR(100),
    tempat_lahir VARCHAR(100),
    tanggal_lahir DATE,

    email VARCHAR(100),
    telepon VARCHAR(20),

    universitas VARCHAR(150),
    fakultas VARCHAR(150),
    program_studi VARCHAR(150),
    semester INT,

    alamat TEXT,
    foto_profil TEXT
);

CREATE TABLE skills (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nama_skill VARCHAR(100) NOT NULL,
    icon VARCHAR(100)
);

CREATE TABLE experiences (
    id INT PRIMARY KEY AUTO_INCREMENT,
    periode VARCHAR(100),
    jabatan VARCHAR(100),
    perusahaan VARCHAR(150),
    deskripsi TEXT
);

CREATE TABLE projects (
    id INT PRIMARY KEY AUTO_INCREMENT,
    judul VARCHAR(255) NOT NULL,
    deskripsi TEXT,
    tags VARCHAR(255),
    gambar_url TEXT
);

CREATE TABLE contacts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nama VARCHAR(100),
    email VARCHAR(100),
    subjek VARCHAR(150),
    pesan TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);