open Alcotest
module Parser = Lib.Parser.Process
module Postgres = Lib.Postgres

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
         "test_composite"
         [
           Postgres.Parameter.make_parameter "field_one"
             (Postgres.Types.Primitive Postgres.Types.Text);
           Postgres.Parameter.make_parameter "field_two"
             (Postgres.Types.Primitive Postgres.Types.Integer);
           Postgres.Parameter.make_parameter "field_three"
             (Postgres.Types.Primitive Postgres.Types.TimestampWithTimeZone);
         ])

let tests = ("Composites", [ test_case "composite" `Quick multiple_fields ])
