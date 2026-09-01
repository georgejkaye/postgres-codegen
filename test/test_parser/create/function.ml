open Alcotest
module Parser = Lib.Parser.Process
module Postgres = Lib.Postgres

let no_args () =
  let input =
    {|
      CREATE FUNCTION test_function ()
      RETURNS TEXT
      LANGUAGE sql
      AS
      SELECT * FROM test_table;
    |}
  in
  Process.test_parser ~input
    ~expected:
      (Postgres.Statement.make_create_function ~or_replace:false "TEST_FUNCTION"
         (Postgres.Types.Primitive Postgres.Types.Text) [] Postgres.Language.Sql
         "SELECT * FROM test_table")

let or_replace () =
  let input =
    {|
      CREATE OR REPLACE FUNCTION test_function ()
      RETURNS TEXT
      LANGUAGE sql
      AS
      SELECT * FROM test_table;
    |}
  in
  Process.test_parser ~input
    ~expected:
      (Postgres.Statement.make_create_function ~or_replace:true "TEST_FUNCTION"
         (Postgres.Types.Primitive Postgres.Types.Text) [] Postgres.Language.Sql
         "SELECT * FROM test_table")

let one_arg () =
  let input =
    {|
      CREATE FUNCTION test_function (
        p_arg_one TEXT
      )
      RETURNS TEXT
      LANGUAGE sql
      AS
      SELECT * FROM test_table;
    |}
  in
  Process.test_parser ~input
    ~expected:
      (Postgres.Statement.make_create_function ~or_replace:false "TEST_FUNCTION"
         (Postgres.Types.Primitive Postgres.Types.Text)
         [
           Postgres.Parameter.make_parameter "P_ARG_ONE"
             (Postgres.Types.Primitive Postgres.Types.Text);
         ]
         Postgres.Language.Sql "SELECT * FROM test_table")

let multiple_args () =
  let input =
    {|
      CREATE FUNCTION test_function (
        p_arg_one TEXT,
        p_arg_two INTEGER_NOTNULL,
        p_arg_three test_composite_notnull[]
      )
      RETURNS TEXT
      LANGUAGE sql
      AS
      SELECT * FROM test_table;
    |}
  in
  Process.test_parser ~input
    ~expected:
      (Postgres.Statement.make_create_function ~or_replace:false "TEST_FUNCTION"
         (Postgres.Types.Primitive Postgres.Types.Text)
         [
           Postgres.Parameter.make_parameter "P_ARG_ONE"
             (Postgres.Types.Primitive Postgres.Types.Text);
           Postgres.Parameter.make_parameter "P_ARG_TWO"
             (Postgres.Types.Notnull
                (Postgres.Types.Primitive Postgres.Types.Integer));
           Postgres.Parameter.make_parameter "P_ARG_THREE"
             (Postgres.Types.Array
                (Postgres.Types.Notnull
                   (Postgres.Types.Composite "TEST_COMPOSITE")));
         ]
         Postgres.Language.Sql "SELECT * FROM test_table")

let multiple_args_oneline () =
  let input =
    {|
      CREATE FUNCTION test_function (
        p_arg_one TEXT, p_arg_two INTEGER_NOTNULL, p_arg_three test_composite_notnull[]
      )
      RETURNS TEXT
      LANGUAGE sql
      AS
      SELECT * FROM test_table;
    |}
  in
  Process.test_parser ~input
    ~expected:
      (Postgres.Statement.make_create_function ~or_replace:false "TEST_FUNCTION"
         (Postgres.Types.Primitive Postgres.Types.Text)
         [
           Postgres.Parameter.make_parameter "P_ARG_ONE"
             (Postgres.Types.Primitive Postgres.Types.Text);
           Postgres.Parameter.make_parameter "P_ARG_TWO"
             (Postgres.Types.Notnull
                (Postgres.Types.Primitive Postgres.Types.Integer));
           Postgres.Parameter.make_parameter "P_ARG_THREE"
             (Postgres.Types.Array
                (Postgres.Types.Notnull
                   (Postgres.Types.Composite "TEST_COMPOSITE")));
         ]
         Postgres.Language.Sql "SELECT * FROM test_table")

let complex_return () =
  let input =
    {|
      CREATE FUNCTION test_function (
        p_arg_one TEXT
      )
      RETURNS TEXT_NOTNULL[]
      LANGUAGE sql
      AS
      SELECT * FROM test_table;
    |}
  in
  Process.test_parser ~input
    ~expected:
      (Postgres.Statement.make_create_function ~or_replace:false "TEST_FUNCTION"
         (Postgres.Types.Array
            (Postgres.Types.Notnull
               (Postgres.Types.Primitive Postgres.Types.Text)))
         [
           Postgres.Parameter.make_parameter "P_ARG_ONE"
             (Postgres.Types.Primitive Postgres.Types.Text);
         ]
         Postgres.Language.Sql "SELECT * FROM test_table")

let plpgsql () =
  let input =
    {|
      CREATE FUNCTION test_function (
        p_arg_one TEXT
      )
      RETURNS TEXT
      LANGUAGE plpgsql
      AS
      $$
      DECLARE
        v_var_one TEXT;
      BEGIN
        v_var_one := SELECT * FROM test_table;
      END;
      $$;
    |}
  in
  Process.test_parser ~input
    ~expected:
      (Postgres.Statement.make_create_function ~or_replace:false "TEST_FUNCTION"
         (Postgres.Types.Primitive Postgres.Types.Text)
         [
           Postgres.Parameter.make_parameter "P_ARG_ONE"
             (Postgres.Types.Primitive Postgres.Types.Text);
         ]
         Postgres.Language.Plpgsql
         "DECLARE\n\
         \        v_var_one TEXT;\n\
         \      BEGIN\n\
         \        v_var_one := SELECT * FROM test_table;\n\
         \      END;\n\
         \      ")

let tests =
  ( "Parser.Create.Function",
    [
      test_case "no args" `Quick no_args;
      test_case "or replace" `Quick or_replace;
      test_case "one arg" `Quick one_arg;
      test_case "multiple args" `Quick multiple_args;
      test_case "multiple args oneline" `Quick multiple_args_oneline;
      test_case "complex return" `Quick complex_return;
      test_case "plpgsql" `Quick plpgsql;
    ] )
