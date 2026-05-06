open Core
open Postgres.Composite

module Postgres_composite_parser :
  Object.Postgres_object_parser
    with type t = Postgres.Composite.postgres_composite = struct
  type t = Postgres.Composite.postgres_composite

  let get_statement_regex = "CREATE TYPE (.*) AS \\((.*)\\)"

  let split_field_name_and_type field_string =
    match Util.String.split_on_first_space field_string with
    | None -> None
    | Some (field_name, field_type) ->
        Some
          {
            field_name;
            field_type = Postgres.Types.postgres_type_of_string field_type;
          }

  let split_composite_fields fields =
    let field_strings = Util.String.split_on_commas fields in
    Util.List.map_with_fail field_strings
      ~message:"Could not split field name and type"
      ~f:split_field_name_and_type

  let postgres_object_of_match m =
    let composite_name = Re.Group.get m 1 in
    let composite_fields = Re.Group.get m 2 |> split_composite_fields in
    match composite_fields with
    | Second message ->
        Second
          [%string "Could not get composite: %{Re.Group.get m 0} (%{message})"]
    | First composite_fields -> First { composite_name; composite_fields }
end

module Postgres_composite_parser_processor =
  Processor.Parser_processor (Postgres_composite_parser)
