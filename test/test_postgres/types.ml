open Alcotest
open Core
module Postgres = Lib.Postgres

let testable_postgres_type =
  testable Postgres.Types.pp_postgres_type (fun a b ->
      Int.equal (Postgres.Types.compare_postgres_type a b) 0)

let test_postgres_type_of_string input expected =
  check testable_postgres_type
    [%string "testable_postgres_type_of_string_%{input}"]
    (Postgres.Types.postgres_type_of_string input)
    expected

let test_void () =
  test_postgres_type_of_string "void"
    (Postgres.Types.Primitive Postgres.Types.Void)

let test_void_caps () =
  test_postgres_type_of_string "VOID"
    (Postgres.Types.Primitive Postgres.Types.Void)

let tests =
  ( "Postgres.Types",
    [
      test_case "void" `Quick test_void;
      test_case "void_caps" `Quick test_void_caps;
    ] )
