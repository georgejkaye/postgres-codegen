open Alcotest
module Parser = Lib.Parser.Process
module Postgres = Lib.Postgres

let single_field () =
  let input =
    {|
      CREATE TYPE test_composite AS (
          field_one TEXT
      );
  |}
  in
  Process.test_parser ~input
    ~expected:
      (Postgres.Statement.make_create_composite ~or_replace:false
         "TEST_COMPOSITE"
         [
           Postgres.Parameter.make_parameter "FIELD_ONE"
             (Postgres.Types.Primitive Postgres.Types.Text);
         ])

let or_replace () =
  let input =
    {|
      CREATE OR REPLACE TYPE test_composite AS (
          field_one TEXT
      );
  |}
  in
  Process.test_parser ~input
    ~expected:
      (Postgres.Statement.make_create_composite ~or_replace:true
         "TEST_COMPOSITE"
         [
           Postgres.Parameter.make_parameter "FIELD_ONE"
             (Postgres.Types.Primitive Postgres.Types.Text);
         ])

let multiple_fields () =
  let input =
    {|
      CREATE TYPE test_composite AS (
          field_one TEXT,
          field_two INTEGER,
          field_three TIMESTAMP WITH TIME ZONE
      );
  |}
  in
  Process.test_parser ~input
    ~expected:
      (Postgres.Statement.make_create_composite ~or_replace:false
         "TEST_COMPOSITE"
         [
           Postgres.Parameter.make_parameter "FIELD_ONE"
             (Postgres.Types.Primitive Postgres.Types.Text);
           Postgres.Parameter.make_parameter "FIELD_TWO"
             (Postgres.Types.Primitive Postgres.Types.Integer);
           Postgres.Parameter.make_parameter "FIELD_THREE"
             (Postgres.Types.Primitive Postgres.Types.TimestampWithTimeZone);
         ])

let multiple_fields_complex_types () =
  let input =
    {|
      CREATE TYPE test_composite AS (
          field_one TEXT[],
          field_two test_composite_notnull,
          field_three integer_notnull[]
      );
  |}
  in
  Process.test_parser ~input
    ~expected:
      (Postgres.Statement.make_create_composite ~or_replace:false
         "TEST_COMPOSITE"
         [
           Postgres.Parameter.make_parameter "FIELD_ONE"
             (Postgres.Types.Array
                (Postgres.Types.Primitive Postgres.Types.Text));
           Postgres.Parameter.make_parameter "FIELD_TWO"
             (Postgres.Types.Notnull (Postgres.Types.Composite "TEST_COMPOSITE"));
           Postgres.Parameter.make_parameter "FIELD_THREE"
             (Postgres.Types.Array
                (Postgres.Types.Notnull
                   (Postgres.Types.Primitive Postgres.Types.Integer)));
         ])

let lowercase () =
  let input =
    {|
      create type test_composite as (
          field_one text,
          field_two integer,
          field_three timestamp with time zone
      );
  |}
  in
  Process.test_parser ~input
    ~expected:
      (Postgres.Statement.make_create_composite ~or_replace:false
         "TEST_COMPOSITE"
         [
           Postgres.Parameter.make_parameter "FIELD_ONE"
             (Postgres.Types.Primitive Postgres.Types.Text);
           Postgres.Parameter.make_parameter "FIELD_TWO"
             (Postgres.Types.Primitive Postgres.Types.Integer);
           Postgres.Parameter.make_parameter "FIELD_THREE"
             (Postgres.Types.Primitive Postgres.Types.TimestampWithTimeZone);
         ])

let tests =
  ( "Parser.Create.Composite",
    [
      test_case "composite single field" `Quick single_field;
      test_case "composite or replace" `Quick or_replace;
      test_case "composite multiple fields" `Quick multiple_fields;
      test_case "composite complex fields" `Quick multiple_fields_complex_types;
      test_case "lowercase" `Quick lowercase;
    ] )
