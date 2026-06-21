open Alcotest

let () =
  run "Postgres_codegen"
    [
      Test_postgres.Types.tests;
      Test_parser.Create.Composite.tests;
      Test_parser.Create.Function.tests;
      Test_parser.Drop.tests;
    ]
