type postgres_function_parameter = {
  parameter_name : string;
  parameter_type : Types.postgres_type;
}

type postgres_function = {
  function_name : string;
  function_return : string;
  function_parameters : postgres_function_parameter list;
}

module Function_postgres_object : Object.Postgres_object = struct
  type t = postgres_function

  let get_name f = f.function_name

  let get_drop_statement f =
    [%string "DROP FUNCTION IF EXISTS %{f.function_name} CASCADE;"]
end
