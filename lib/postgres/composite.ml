type postgres_composite_field = {
  field_name : string;
  field_type : Types.postgres_type;
}

type postgres_composite = {
  composite_name : string;
  composite_fields : postgres_composite_field list;
}

module Composite_postgres_object : Object.Postgres_object = struct
  type t = postgres_composite

  let get_name c = c.composite_name

  let get_drop_statement c =
    [%string "DROP TYPE IF EXISTS %{c.composite_name} CASCADE;"]
end
