CREATE FUNCTION test_function (p_one TEXT)
RETURNS SETOF details_detal
LANGUAGE sql
AS
SELECT 1 FROM DUAL;
--test
CREATE FUNCTION test_function2 (p_two TEXT_NOTNULL, p_three INTEGER[])
RETURNS SETOF details_detal
LANGUAGE sql
AS
$$
DECLARE
    v_four TEXT ----test
BEGIN
    INSERT INTO test (c_one) VALUES (v_four);
END;
$$;