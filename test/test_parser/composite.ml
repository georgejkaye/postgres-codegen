open Alcotest
module Parser = Lib.Parser.Process

let pp_result pp_ok pp_error = function
  | Ok v -> pp_ok v
  | Error e -> pp_error e

let test_parse_composite () =
  let test_composite =
    {|
      CREATE TYPE test_composite AS (
          field_one TEXT,
          field_two NUMBER,
          field_three TIMESTAMP WITH TIME ZONE
      );
  |}
  in

  let result = Parser.parse_statements test_composite in
  match result with
  | Error _ -> failwith "No result"
  | Ok statements -> (
      let _ = (check int) "number of results" (List.length statements) 1 in
      let result_object = List.hd statements in
      match result_object with
      | None -> failwith "No result"
      | Some s ->
          check Test_postgres.Statement.testable_postgres_statement
            "test_parse_composite" s Lib.Postgres.Statement.Create
            { object_data })
