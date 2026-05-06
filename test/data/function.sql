CREATE FUNCTION test_function (
    p_arg_one INTEGER,
    p_arg_two TEXT,
    p_arg_three TIMESTAMP WITH TIME ZONE
)
RETURNS INTEGER
LANGUAGE sql
AS
$$
SELECT * FROM test_table;
$$;