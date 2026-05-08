type postgres_composite_field = {
  field_name : string;
  field_type : Types.postgres_type;
}
[@@deriving show]

type postgres_composite = {
  composite_name : string;
  composite_fields : postgres_composite_field list;
}
[@@deriving show]

module Postgres_composite :
  Object_t.Postgres_object_t with type t = postgres_composite = struct
  type t = postgres_composite

  let get_object_type_name = "composite"
  let get_name c = c.composite_name

  let get_drop_statement c =
    [%string "DROP TYPE IF EXISTS %{c.composite_name} CASCADE;"]
end
