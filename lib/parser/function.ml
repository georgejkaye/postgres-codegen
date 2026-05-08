open Postgres.Function
open Core
open Util

module Postgres_function_parser : Object.Postgres_object_parser_t = struct
  type t = Postgres.Function.postgres_function

  let get_object_type_name = "function"

  let get_statement_regex =
    "CREATE(?: OR REPLACE)? FUNCTION ([A-z_]*)(?: \
     )?\\((.*)\\).*RETURNS(?:SETOF)? (.*?) LANGUAGE (.*?) AS $$(.*)$$"

  let split_parameter_name_and_type parameter_string =
    match parameter_string |> String.strip |> String.split_on_first_space with
    | None -> None
    | Some (parameter_name, parameter_type) ->
        let parameter_type, _ =
          String.split_on_pattern parameter_type " DEFAULT"
        in
        Some
          {
            parameter_name;
            parameter_type =
              Postgres.Types.postgres_type_of_string parameter_type;
          }

  let split_parameters s =
    if phys_equal s "" then First []
    else
      let arg_strings = String.split_on_commas s in
      List.map_with_fail arg_strings
        ~message:"Could not split parameter name and type"
        ~f:split_parameter_name_and_type

  let of_match m =
    let function_name = Re.Group.get m 1 in
    let function_parameters = Re.Group.get m 2 |> split_parameters in
    let function_return =
      Re.Group.get m 3 |> Postgres.Types.postgres_type_of_string
    in
    let function_language_string = Re.Group.get m 4 in
    let function_language =
      Postgres.Language.of_string function_language_string
    in
    match function_parameters with
    | Second message ->
        Second
          [%string "Could not get function: %{Re.Group.get m 0} (%{message})"]
    | First function_parameters -> (
        match function_language with
        | None ->
            Second
              [%string
                "Could not get function language: %{function_language_string}"]
        | Some function_language ->
            First
              {
                function_name;
                function_return;
                function_parameters;
                function_language;
              })

  let to_object f = Postgres.Object.Function f
end

module Postgres_function = struct
  include Postgres.Function.Postgres_function
  include Make.Make_parser (Postgres_function_parser)
end
