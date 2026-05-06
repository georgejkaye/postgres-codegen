open Core

module Parser_processor (P : Object.Postgres_object_parser) : sig
  val get_postgres_objects_for_postgres_file_string : string -> P.t list
end = struct
  let normalise_file_string contents =
    String.substr_replace_all contents ~pattern:"\n" ~with_:" "

  let get_postgres_object_for_statement statement =
    let re = Re.compile (Re.Perl.re P.get_statement_regex) in
    match Re.exec_opt re statement with
    | None ->
        Second [%string "Could not parse object from statement: %{statement}"]
    | Some m -> P.postgres_object_of_match m

  let get_postgres_objects_for_postgres_file_string file_string =
    file_string |> normalise_file_string |> Util.String.split_on_semicolons
    |> List.map ~f:get_postgres_object_for_statement
    |> List.fold_right
         ~f:(fun cur acc ->
           match cur with First res -> res :: acc | Second _ -> acc)
         ~init:[]
end
