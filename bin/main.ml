open Postgres_codegen
open Core
open Util

let () =
  let function_file_contents =
    File.Concrete.Base_file_wrapper.read_file
      "../train-tracker/db/code/functions/select/train/leg.sql"
  in
  function_file_contents
  |> Parser.Process.get_postgres_objects_for_file_contents
  |> List.iter ~f:(Show.show_line Postgres.Object.show_postgres_object)
