type postgres_object =
  | Composite of Composite.postgres_composite
  | Domain of Domain.postgres_domain
  | Function of Function.postgres_function
[@@deriving show]

module Postgres_object :
  Object_t.Postgres_object_t with type t = postgres_object = struct
  type t = postgres_object

  let get_name = function
    | Composite c -> Composite.Postgres_composite.get_name c
    | Domain d -> Domain.Postgres_domain.get_name d
    | Function f -> Function.Postgres_function.get_name f

  let get_drop_statement = function
    | Composite c -> Composite.Postgres_composite.get_drop_statement c
    | Domain d -> Domain.Postgres_domain.get_drop_statement d
    | Function f -> Function.Postgres_function.get_drop_statement f
end
