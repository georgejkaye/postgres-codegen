type postgres_function_parameter = {
  parameter_name : string;
  parameter_type : Types.postgres_type;
}
[@@deriving show]

type postgres_function = {
  function_name : string;
  function_return : Types.postgres_type;
  function_parameters : postgres_function_parameter list;
  function_language : Language.language;
}
[@@deriving show]
