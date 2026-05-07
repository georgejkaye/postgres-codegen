type postgres_function_parameter = {
  parameter_name : string;
  parameter_type : Types.postgres_type;
}
[@@deriving show]

type postgres_function = {
  function_name : string;
  function_return : Types.postgres_type;
  function_parameters : postgres_function_parameter list;
}
[@@deriving show]

module Postgres_function :
  Object_t.Postgres_object_t with type t = postgres_function = struct
  type t = postgres_function

  let get_name f = f.function_name

  let get_drop_statement f =
    [%string "DROP FUNCTION IF EXISTS %{f.function_name} CASCADE;"]
end
