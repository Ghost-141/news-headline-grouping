-- Breaking News Queue Table
-- This table stores detected breaking news for similarity-based deduplication before sending

CREATE TABLE IF NOT EXISTS breaking_news_queue (
    id INT AUTO_INCREMENT PRIMARY KEY,
    news_id INT NOT NULL,
    source VARCHAR(100),
    title VARCHAR(255) NOT NULL,
    link VARCHAR(500) NOT NULL UNIQUE,
    publish_time VARCHAR(500),
    sent_status TINYINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (news_id) REFERENCES news(id) ON DELETE CASCADE
);

-- Index for faster queries
CREATE INDEX idx_sent_status ON breaking_news_queue(sent_status);
CREATE INDEX idx_created_at ON breaking_news_queue(created_at);
