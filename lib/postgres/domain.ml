type postgres_domain = {
  domain_name : string;
  underlying_type : Types.postgres_type;
}

module Function_postgres_object : Object.Postgres_object = struct
  type t = postgres_domain

  let get_name f = f.domain_name

  let get_drop_statement f =
    [%string "DROP DOMAIN IF EXISTS %{f.domain_name} CASCADE;"]
end
