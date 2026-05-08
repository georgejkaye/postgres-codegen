open Core
open Util

let normalise_file_string contents =
  String.substr_replace_all contents ~pattern:"\n" ~with_:" "

let get_statements file_contents =
  file_contents
  |> normalise_file_string
  |> String.split_on_semicolons
  |> List.map ~f:String.strip
  |> List.filter ~f:(fun x -> String.length x > 0)

let get_object p statement =
  let module P = (val p : Make.Make_parser_t) in
  P.object_of_statement statement

let try_get_objects ps statement =
  List.fold ps
    ~f:(fun res p ->
      match res with Second _ -> get_object p statement | x -> x)
    ~init:(Second [%string "Could not get object for %{statement}"])

let get_postgres_object_for_statement =
  try_get_objects
    [
      (module Composite.Postgres_composite);
      (module Domain.Postgres_domain);
      (module Function.Postgres_function);
    ]

let get_postgres_objects_for_statements =
  List.map ~f:get_postgres_object_for_statement

let get_postgres_objects_for_file_contents file_contents =
  file_contents |> get_statements |> get_postgres_objects_for_statements
