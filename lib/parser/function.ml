open Core
open Postgres.Function

module Postgres_function_parser :
  Object.Postgres_object_parser
    with type t = Postgres.Function.postgres_function = struct
  type t = Postgres.Function.postgres_function

  let get_statement_regex =
    "CREATE(?: OR REPLACE)? FUNCTION ([A-z_]*)(?: \
     )?\\((.*)\\).*RETURNS(?:SETOF)? (.*?) LANGUAGE"

  let split_parameter_name_and_type parameter_string =
    match
      parameter_string |> String.strip |> Util.String.split_on_first_space
    with
    | None -> None
    | Some (parameter_name, parameter_type) ->
        let parameter_type, _ = Util.String.split parameter_type " DEFAULT" in
        Some
          {
            parameter_name;
            parameter_type =
              Postgres.Types.postgres_type_of_string parameter_type;
          }

  let split_parameters s =
    if phys_equal s "" then First []
    else
      let arg_strings = Util.String.split_on_commas s in
      Util.List.map_with_fail arg_strings
        ~message:"Could not split parameter name and type"
        ~f:split_parameter_name_and_type

  let postgres_object_of_match m =
    let function_name = Re.Group.get m 1 in
    let function_parameters = Re.Group.get m 2 |> split_parameters in
    let function_return = Re.Group.get m 3 in
    match function_parameters with
    | Second message ->
        Second
          [%string "Could not get function: %{Re.Group.get m 0} (%{message})"]
    | First function_parameters ->
        First { function_name; function_return; function_parameters }
end

module Postgres_function_parser_processor =
  Processor.Parser_processor (Postgres_function_parser)
