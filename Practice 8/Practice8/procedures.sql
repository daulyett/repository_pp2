#1 UPSERT
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;

#4 DELETE
CREATE OR REPLACE PROCEDURE delete_contact_proc(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF p_name IS NOT NULL THEN
        DELETE FROM contacts WHERE name = p_name;
    ELSIF p_phone IS NOT NULL THEN
        DELETE FROM contacts WHERE phone = p_phone;
    END IF;
END;
$$;

#5 BULK INSERT
CREATE OR REPLACE PROCEDURE insert_many_contacts(names TEXT[], phones TEXT[])
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(names, 1)
    LOOP
        IF length(phones[i]) >= 10 THEN
            INSERT INTO contacts(name, phone)
            VALUES(names[i], phones[i]);
        ELSE
            RAISE NOTICE 'Invalid phone: %', phones[i];
        END IF;
    END LOOP;
END;
$$;