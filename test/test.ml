open Alcotest
open Test_postgres
open Test_parser

let () =
  run "Test"
    [
      ( "test",
        [ test_case "test" `Quick Test_parser.Composite.test_parse_composite ]
      );
    ]
