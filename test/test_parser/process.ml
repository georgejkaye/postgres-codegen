open Alcotest
module Parser = Lib.Parser.Process
module Postgres = Lib.Postgres

let test_parser ~input ~expected =
  let result = Parser.parse_statements input in
  match result with
  | Error _ -> failwith "No result"
  | Ok statements -> (
      let _ = (check int) "number of results" (List.length statements) 1 in
      let result_object = List.hd statements in
      match result_object with
      | None -> failwith "No result"
      | Some s ->
          check Test_postgres.Statement.testable_postgres_statement
            "test_parse_composite" s expected)
