-- Habilitar UUIDs (opcional pero recomendado para producción)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. CATÁLOGO DE PRODUCTOS (Lo que vendes)
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. CLIENTES / LEADS (Tu "Source of Truth")
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20), -- Teléfono normalizado (+51...)
    status VARCHAR(20) DEFAULT 'new', -- new, qualified, customer, churned
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. IDENTIDADES SOCIALES (La magia Multi-canal)
CREATE TABLE social_identities (
    platform_id VARCHAR(100) NOT NULL, -- El ID que te da Meta/Telegram (ej: 519999999@c.us)
    platform VARCHAR(20) NOT NULL,     -- 'whatsapp', 'telegram', 'messenger'
    customer_id INTEGER REFERENCES customers(id) ON DELETE CASCADE,
    last_interaction_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (platform_id, platform)
);

-- 4. ÓRDENES DE VENTA
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    channel VARCHAR(20), 
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending', 
    stripe_payment_link VARCHAR(255),    
    stripe_payment_id VARCHAR(100),    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. ITEMS DE LA ORDEN
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) GENERATED ALWAYS AS (quantity * unit_price) STORED
);
