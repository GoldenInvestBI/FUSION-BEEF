-- Seed products from Minerva (Bovinos Premium category)
-- Prices already include 60% markup

INSERT INTO products (
  sku, name, category, priceOriginal, priceWithMarkup, markup,
  imageUrl, imageLocalPath, stockStatus, minervaUrl, inStock,
  lastScrapedAt, createdAt, updatedAt
) VALUES
-- 1. Paleta Shoulder
('500100318', 'Racas Britanicas Paleta Shoulder Brasil Cabaña Las Lilas Grass Fed Resfriado', 'Bovinos Premium', '66.99', '107.18', '60', 
 'https://meuminerva.com/media/catalog/product/5/0/500100318.jpg', '/images/products/500100318.jpg', 'RESFRIADO',
 'https://meuminerva.com/racas-britanicas-paleta-shoulder-brasil-cabana-las-lilas-grass-fed-resfriado-500100318.html', 1,
 NOW(), NOW(), NOW()),

-- 2. Maminha Uruguay
('200004423', 'Angus Maminha Uruguay Cabaña Las Lilas Grass Fed Resfriado', 'Bovinos Premium', '67.99', '108.78', '60',
 'https://meuminerva.com/media/catalog/product/2/0/200004423.jpg', '/images/products/200004423.jpg', 'RESFRIADO',
 'https://meuminerva.com/angus-maminha-uruguay-cabana-las-lilas-grass-fed-resfriado-200004423.html', 1,
 NOW(), NOW(), NOW()),

-- 3. Fralda Brasil
('500100446', 'Novilho Fralda Brasil Cabaña Las Lilas Grass Fed Resfriado', 'Bovinos Premium', '56.99', '91.18', '60',
 'https://meuminerva.com/media/catalog/product/5/0/500100446.jpg', '/images/products/500100446.jpg', 'RESFRIADO',
 'https://meuminerva.com/novilho-fralda-brasil-cabana-las-lilas-grass-fed-resfriado-500100446.html', 1,
 NOW(), NOW(), NOW()),

-- 4. Ancho Brasil
('500100432', 'Novilho Ancho Brasil Cabaña Las Lilas Grass Fed Resfriado', 'Bovinos Premium', '79.99', '127.98', '60',
 'https://meuminerva.com/media/catalog/product/5/0/500100432.jpg', '/images/products/500100432.jpg', 'RESFRIADO',
 'https://meuminerva.com/novilho-ancho-brasil-cabana-las-lilas-grass-fed-resfriado-500100432.html', 1,
 NOW(), NOW(), NOW()),

-- 5. Fralda Red Brasil
('500100445', 'Novilho Fralda Red Brasil Cabaña Las Lilas Grass Fed Resfriado', 'Bovinos Premium', '78.98', '126.37', '60',
 'https://meuminerva.com/media/catalog/product/5/0/500100445.jpg', '/images/products/500100445.jpg', 'RESFRIADO',
 'https://meuminerva.com/novilho-fralda-red-brasil-cabana-las-lilas-grass-fed-resfriado-500100445.html', 1,
 NOW(), NOW(), NOW()),

-- 6. Paleta Coração
('500100435', 'Novilho Paleta Coração Brasil Cabaña Las Lilas Grass Fed Resfriado', 'Bovinos Premium', '54.98', '87.97', '60',
 'https://meuminerva.com/media/catalog/product/5/0/500100435.jpg', '/images/products/500100435.jpg', 'RESFRIADO',
 'https://meuminerva.com/novilho-paleta-coracao-brasil-cabana-las-lilas-grass-fed-resfriado-500100435.html', 1,
 NOW(), NOW(), NOW()),

-- 7. Picanha Leve
('500100423', 'Novilho Picanha Leve Brasil Cabaña Las Lilas Grain Fed Resfriado', 'Bovinos Premium', '114.99', '183.98', '60',
 'https://meuminerva.com/media/catalog/product/5/0/500100423.jpg', '/images/products/500100423.jpg', 'RESFRIADO',
 'https://meuminerva.com/novilho-picanha-leve-brasil-cabana-las-lilas-grain-fed-resfriado-500100423.html', 1,
 NOW(), NOW(), NOW()),

-- 8. Acem Brasil
('500100437', 'Novilho Acem Brasil Cabaña Las Lilas Grass Fed Resfriado', 'Bovinos Premium', '51.98', '83.17', '60',
 'https://meuminerva.com/media/catalog/product/5/0/500100437.jpg', '/images/products/500100437.jpg', 'RESFRIADO',
 'https://meuminerva.com/novilho-acem-brasil-cabana-las-lilas-grass-fed-resfriado-500100437.html', 1,
 NOW(), NOW(), NOW()),

-- 9. Filé Mignon
('500100273', 'Novilho File Mignon Brasil Cabaña Las Lilas Grass Fed Resfriado', 'Bovinos Premium', '76.99', '123.18', '60',
 'https://meuminerva.com/media/catalog/product/5/0/500100273.jpg', '/images/products/500100273.jpg', 'RESFRIADO',
 'https://meuminerva.com/novilho-file-mignon-brasil-cabana-las-lilas-grass-fed-resfriado-500100273.html', 1,
 NOW(), NOW(), NOW()),

-- 10. Fralda Red Grass Fed
('500100282', 'Novilho Fralda Red Brasil Cabaña Las Lilas Grass Fed Resfriado', 'Bovinos Premium', '61.99', '99.18', '60',
 'https://meuminerva.com/media/catalog/product/5/0/500100282.jpg', '/images/products/500100282.jpg', 'RESFRIADO',
 'https://meuminerva.com/novilho-fralda-red-brasil-cabana-las-lilas-grass-fed-resfriado-500100282.html', 1,
 NOW(), NOW(), NOW()),

-- 11. Chorizo Brasil
('500100265', 'Novilho Chorizo Brasil Cabaña Las Lilas Grass Fed Resfriado', 'Bovinos Premium', '49.99', '79.98', '60',
 'https://meuminerva.com/media/catalog/product/5/0/500100265.jpg', '/images/products/500100265.jpg', 'RESFRIADO',
 'https://meuminerva.com/novilho-chorizo-brasil-cabana-las-lilas-grass-fed-resfriado-500100265.html', 1,
 NOW(), NOW(), NOW()),

-- 12. Fralda Grass Fed
('500100281', 'Novilho Fralda Brasil Cabaña Las Lilas Grass Fed Resfriado', 'Bovinos Premium', '46.99', '75.18', '60',
 'https://meuminerva.com/media/catalog/product/5/0/500100281.jpg', '/images/products/500100281.jpg', 'RESFRIADO',
 'https://meuminerva.com/novilho-fralda-brasil-cabana-las-lilas-grass-fed-resfriado-500100281.html', 1,
 NOW(), NOW(), NOW())

ON DUPLICATE KEY UPDATE
  name = VALUES(name),
  priceOriginal = VALUES(priceOriginal),
  priceWithMarkup = VALUES(priceWithMarkup),
  inStock = VALUES(inStock),
  lastScrapedAt = NOW(),
  updatedAt = NOW();

-- Insert default markup setting
INSERT INTO settings (key, value, description, updatedAt)
VALUES ('default_markup', '60', 'Default markup percentage for all products', NOW())
ON DUPLICATE KEY UPDATE value = VALUES(value), updatedAt = NOW();
