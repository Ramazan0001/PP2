CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p text)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT phonebook.id, phonebook.name, phonebook.phone
    FROM phonebook
    WHERE phonebook.name ILIKE '%' || p || '%'
       OR phonebook.phone ILIKE '%' || p || '%';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT phonebook.id, phonebook.name, phonebook.phone
    FROM phonebook
    ORDER BY phonebook.id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;