open Postgres.Composite
open Core
open Util

module Postgres_composite_parser : Object.Postgres_object_parser_t = struct
  type t = postgres_composite

  let get_statement_regex = "CREATE(?: OR REPLACE)? TYPE (.*) AS \\((.*)\\)"

  let split_field_name_and_type field_string =
    field_string |> String.strip |> String.split_on_first_space |> function
    | None -> None
    | Some (field_name, field_type) ->
        Some
          {
            field_name = field_name |> String.strip;
            field_type =
              field_type
              |> String.strip
              |> Postgres.Types.postgres_type_of_string;
          }

  let split_composite_fields fields =
    let field_strings = String.split_on_commas fields in
    List.map_with_fail field_strings
      ~message:"Could not split field name and type"
      ~f:split_field_name_and_type

  let of_match m =
    let composite_name = Re.Group.get m 1 in
    let composite_fields = Re.Group.get m 2 |> split_composite_fields in
    match composite_fields with
    | Second message ->
        Second
          [%string "Could not get composite: %{Re.Group.get m 0} (%{message})"]
    | First composite_fields -> First { composite_name; composite_fields }

  let to_object o = Postgres.Object.Composite o
end

module Postgres_composite = struct
  include Postgres_composite
  include Make.Make_parser (Postgres_composite_parser)
end
