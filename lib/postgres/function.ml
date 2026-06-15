open Core

type postgres_function = {
  function_name : string;
  function_return : Types.postgres_type;
  function_parameters : Parameter.parameter list;
  function_language : Language.language;
  function_body : string;
}
[@@deriving show, compare]
