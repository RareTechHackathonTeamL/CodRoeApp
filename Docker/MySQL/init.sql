DROP DATABASE chatapp;
DROP USER 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp;
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';

CREATE TABLE companies (
    id VARCHAR(255) PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_at DATETIME
);

CREATE TABLE users (
    user_id VARCHAR(255) PRIMARY KEY,
    user_name VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    icon_img VARCHAR(255),
    --  company_id VARCHAR(255),
    -- nickname VARCHAR(255),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_at DATETIME
    -- FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE 
);

CREATE TABLE chat (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    chat_name VARCHAR(255) UNIQUE NOT NULL,
    detail VARCHAR(255),
    chat_type INT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_at DATETIME,
    latest_messages DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE messages (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    chat_id VARCHAR(255) NOT NULL,
    message TEXT,
    stamp_id VARCHAR(255),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (chat_id) REFERENCES chat(id) ON DELETE CASCADE
);

CREATE TABLE members (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    chat_id VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (chat_id) REFERENCES chat(id) ON DELETE CASCADE
);

CREATE TABLE stamps (
    id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    stamp_path VARCHAR(255) NOT NULL,
    move_stamp BOOLEAN,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_at DATETIME
);

INSERT INTO users(user_id, user_name, email, password, icon_img, created_at) VALUES('a', 'テスト', 'demota@gmail.com', 'a', 'default_image.png', '2025-07-01');
INSERT INTO chat(id, user_id, chat_name, detail, chat_type, created_at, latest_messages) VALUES('aaaaaaaaaa', 'a', '明太子を語る会', "明太子について語りましょう！！", 0, '2025-07-01','2025-07-01');
INSERT INTO chat(id, user_id, chat_name, detail, chat_type, created_at, latest_messages) VALUES('bbbbbbbbbb', 'a', 'スケトウダラを語る会', "スケトウダラについてダラダラ語りましょう！！", 0, '2025-07-02', '2025-07-02');
INSERT INTO messages(id, user_id, chat_id, message, created_at) VALUES('c', 'a', 'aaaaaaaaaa', '私は辛さ控えめかつ、塩味が強めが好きだなぁ', '2025-07-01');
INSERT INTO stamps(id, title, stamp_path, created_at) VALUES
('first_stamp1_20250801', 'おつかれんたいこ〜', 'img/stamps/mentai1.png', '2025-08-01'),
('first_stamp2_20250801', 'おやすみめんたいちゃん', 'img/stamps/mentai2.png', '2025-08-01'),
('first_stamp3_20250801', 'ごめんたいこ', 'img/stamps/mentai3.png', '2025-08-01'),
('first_stamp4_20250801', 'ねむいめんたいちゃん', 'img/stamps/mentai4.png', '2025-08-01'),
('first_stamp5_20250801', 'メガネめんたいちゃん', 'img/stamps/mentai5.png', '2025-08-01'),
('first_stamp6_20250801', 'めんこいい', 'img/stamps/mentai6.png', '2025-08-01'),
('first_stamp7_20250801', 'めんこいめんこい', 'img/stamps/mentai7.png', '2025-08-01'),
('first_stamp8_20250801', 'やったーめんたいちゃん', 'img/stamps/mentai8.png', '2025-08-01'),
('first_stamp9_20250801', 'やったらこ', 'img/stamps/mentai9.png', '2025-08-01'),
('first_stamp10_20250801', '帰宅めんたいちゃん', 'img/stamps/mentai10.png', '2025-08-01'),
('first_stamp11_20250801', '手を振るめんたいちゃん', 'img/stamps/mentai11.png', '2025-08-01'),
('first_stamp12_20250801', '望遠鏡めんたいちゃん', 'img/stamps/mentai12.png', '2025-08-01');
