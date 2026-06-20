open Alcotest

let () =
  run "Postgres_codegen"
    [ Test_parser.Composite.tests; Test_postgres.Types.tests ]
