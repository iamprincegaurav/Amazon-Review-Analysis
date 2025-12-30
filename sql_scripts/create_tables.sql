CREATE TABLE amazon_reviews (
    id VARCHAR(50),
    brand VARCHAR(100),
    category VARCHAR(255),
    product_name TEXT,
    rating INT,
    review_text TEXT,
    review_title TEXT,
    review_date VARCHAR(100),
    sentiment VARCHAR(20)
);

SELECT brand, AVG(rating) as avg_rating 
FROM amazon_reviews 
GROUP BY brand 
ORDER BY avg_rating DESC;