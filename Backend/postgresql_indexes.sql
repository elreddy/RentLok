-- Properties
CREATE INDEX properties_property_id_hash_idx ON properties USING hash(property_id);

-- Rooms (composite index)
CREATE INDEX rooms_room_property_btree_idx ON rooms(room_id, property_id);

-- Bookings (composite index)
CREATE INDEX bookings_ids_btree_idx ON bookings(booking_id, tenant_id, room_id, property_id);

-- Payments
CREATE INDEX payments_booking_id_hash_idx ON payments USING hash(booking_id);

-- Requests
CREATE INDEX requests_property_id_hash_idx ON requests USING hash(property_id);

-- Tenants
CREATE INDEX tenants_tenant_id_hash_idx ON tenants USING hash(tenant_id);
