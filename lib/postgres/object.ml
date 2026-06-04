type postgres_object =
  | Composite of Composite.postgres_composite
  | Domain of Domain.postgres_domain
  | Function of Function.postgres_function
  | View of View.postgres_view
[@@deriving show]

let get_name = function
  | Composite c -> c.composite_name
  | Domain d -> d.domain_name
  | Function f -> f.function_name
  | View v -> v.view_name

let get_drop_statement = function
  | Composite c -> [%string "DROP TYPE IF EXISTS %{c.composite_name} CASCADE;"]
  | Domain d -> [%string "DROP DOMAIN IF EXISTS %{d.domain_name} CASCADE;"]
  | Function f -> [%string "DROP FUNCTION IF EXISTS %{f.function_name}"]
  | View v -> [%string "DROP VIEW IF EXISTS %{v.view_name}"]
