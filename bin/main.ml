open Postgres_codegen
open Core
open Postgres.Function

let () =
  let function_file_contents =
    File.Concrete.Base_file_wrapper.read_file
      "../train-tracker/db/code/functions/select/train/leg.sql"
  in
  let functions =
    Parser.Function.Postgres_function_parser_processor
    .get_postgres_objects_for_postgres_file_string function_file_contents
  in
  List.iter functions ~f:(fun f -> printf "%s\n" f.function_name);
  let type_file_contents =
    File.Concrete.Base_file_wrapper.read_file
      "../train-tracker/db/code/types/train/leg.sql"
  in
  let types =
    Parser.Composite.Postgres_composite_parser_processor
    .get_postgres_objects_for_postgres_file_string type_file_contents
  in
  List.iter types ~f:(fun f -> printf "%s\n" f.composite_name)
